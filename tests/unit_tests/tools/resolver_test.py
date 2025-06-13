import dataclasses
from unittest.mock import ANY
import pytest

from fastmcp.tools.tool import Tool

from py_conf_mcp.config import (
    FromPythonClassConfig,
    FromPythonFunctionConfig,
    ToolDefinitionsConfig
)
from py_conf_mcp.tools.example.joke import get_joke
from py_conf_mcp.tools.resolver import (
    ConfigToolResolver,
    get_tool_from_python_class,
    get_tool_function_with_dynamic_parameters
)


FROM_PYTHON_CLASS_CONFIG_1 = FromPythonClassConfig(
    name='get_static_content',
    module='py_conf_mcp.tools.sources.static',
    class_name='StaticContentTool',
    init_parameters={
        'content': 'Static content'
    }
)

KWARGS_FROM_PYTHON_CLASS_CONFIG_1 = FromPythonClassConfig(
    name='fetch_web_api',
    module='py_conf_mcp.tools.sources.web_api',
    class_name='WebApiTool',
    init_parameters={
        'url': 'Dummy URL'
    }
)


DEFAULT_TOOL_DEFINITIONS_CONFIG: ToolDefinitionsConfig = ToolDefinitionsConfig(
    from_python_function=[
        FromPythonFunctionConfig(
            name='get_joke',
            module='py_conf_mcp.tools.example.joke',
            key='get_joke'
        )
    ],
    from_python_class=[FROM_PYTHON_CLASS_CONFIG_1]
)

DEFAULT_CONFIG_TOOL_RESOLVER = ConfigToolResolver(
    tool_definitions_config=DEFAULT_TOOL_DEFINITIONS_CONFIG
)


class TestGetToolFunctionWithDynamicParameters:
    def test_should_return_wrapper_dynamic_parameters(
        self
    ):
        def _test_function(**kwargs):
            return kwargs

        tool_fn = get_tool_function_with_dynamic_parameters(
            _test_function,
            inputs={
                'param_1': {
                    'type': 'str',
                    'default': 'default_value_1'
                }
            },
            tool_name='test_tool'
        )
        mcp_tool = Tool.from_function(tool_fn)
        properties_dict = mcp_tool.parameters['properties']
        assert properties_dict == {
            'param_1': {
                'type': 'string',
                'default': 'default_value_1',
                'title': ANY
            }
        }

    def test_should_return_wrapper_with_enum(
        self
    ):
        def _test_function(**kwargs):
            return kwargs

        tool_fn = get_tool_function_with_dynamic_parameters(
            _test_function,
            inputs={
                'param_1': {
                    'type': 'str',
                    'default': 'default_value_1',
                    'enum': ['value_1', 'value_2']
                }
            },
            tool_name='test_tool'
        )
        mcp_tool = Tool.from_function(tool_fn)
        properties_dict = mcp_tool.parameters['properties']
        assert properties_dict == {
            'param_1': {
                'type': 'string',
                'default': 'default_value_1',
                'enum': ['value_1', 'value_2'],
                'title': ANY
            }
        }

    def test_should_return_wrapper_with_title_and_description(
        self
    ):
        def _test_function(**kwargs):
            return kwargs

        tool_fn = get_tool_function_with_dynamic_parameters(
            _test_function,
            inputs={
                'param_1': {
                    'type': 'str',
                    'default': 'default_value_1',
                    'enum': ['value_1', 'value_2'],
                    'title': 'Parameter 1',
                    'description': 'Description of parameter 1'
                }
            },
            tool_name='test_tool'
        )
        mcp_tool = Tool.from_function(tool_fn)
        properties_dict = mcp_tool.parameters['properties']
        assert properties_dict == {
            'param_1': {
                'type': 'string',
                'default': 'default_value_1',
                'enum': ['value_1', 'value_2'],
                'title': 'Parameter 1',
                'description': 'Description of parameter 1'
            }
        }


class TestFromPythonClassConfig:
    def test_should_load_from_class(self):
        tool = get_tool_from_python_class(FROM_PYTHON_CLASS_CONFIG_1)
        assert tool.name == FROM_PYTHON_CLASS_CONFIG_1.name

    def test_should_load_from_class_with_dynamic_parameters(
        self
    ):
        tool = get_tool_from_python_class(dataclasses.replace(
            FROM_PYTHON_CLASS_CONFIG_1,
            inputs={'param_1': {'type': 'str'}}
        ))
        mcp_tool = Tool.from_function(tool.tool_fn)
        properties_dict = mcp_tool.parameters['properties']
        assert properties_dict.keys() == {'param_1'}

    def test_should_create_wrapper_if_dynamic_parameters_are_empty_and_fn_accepts_kwargs(
        self
    ):
        tool = get_tool_from_python_class(dataclasses.replace(
            KWARGS_FROM_PYTHON_CLASS_CONFIG_1,
            inputs={}
        ))
        mcp_tool = Tool.from_function(tool.tool_fn)
        properties_dict = mcp_tool.parameters['properties']
        assert not properties_dict


class TestConfigToolResolver:
    def test_should_raise_error_if_unknown_tool_name(self):
        with pytest.raises(KeyError):
            DEFAULT_CONFIG_TOOL_RESOLVER.get_tool_by_name('unknown')

    def test_should_resolve_get_joke(self):
        tool = DEFAULT_CONFIG_TOOL_RESOLVER.get_tool_by_name('get_joke')
        assert tool.tool_fn == get_joke

    def test_should_resolve_tool_using_tool_class(self):
        tool = DEFAULT_CONFIG_TOOL_RESOLVER.get_tool_by_name('get_static_content')
        assert tool

    def test_should_be_able_to_set_name_and_description_of_tool(self):
        resolver = ConfigToolResolver(
            tool_definitions_config=ToolDefinitionsConfig(
                from_python_function=[FromPythonFunctionConfig(
                    name='new_name',
                    module='py_conf_mcp.tools.example.joke',
                    key='get_joke',
                    description='New description'
                )]
            )
        )
        tool = resolver.get_tool_by_name('new_name')
        assert tool.tool_fn == get_joke
        assert tool.name == 'new_name'
        assert tool.description == 'New description'
