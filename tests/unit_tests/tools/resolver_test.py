import pytest

from py_conf_mcp.config import (
    FromPythonFunctionConfig,
    ToolDefinitionsConfig
)
from py_conf_mcp.tools.example.joke import get_joke
from py_conf_mcp.tools.resolver import ConfigToolResolver


DEFAULT_TOOL_DEFINITIONS_CONFIG: ToolDefinitionsConfig = ToolDefinitionsConfig(
    from_python_function=[
        FromPythonFunctionConfig(
            name='get_joke',
            module='py_conf_mcp.tools.example.joke',
            key='get_joke'
        )
    ]
)

DEFAULT_CONFIG_TOOL_RESOLVER = ConfigToolResolver(
    tool_definitions_config=DEFAULT_TOOL_DEFINITIONS_CONFIG
)


class TestConfigToolResolver:
    def test_should_raise_error_if_unknown_tool_name(self):
        with pytest.raises(KeyError):
            DEFAULT_CONFIG_TOOL_RESOLVER.get_tool_by_name('unknown')

    def test_should_resolve_get_joke(self):
        tool = DEFAULT_CONFIG_TOOL_RESOLVER.get_tool_by_name('get_joke')
        assert tool.tool_fn == get_joke

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
