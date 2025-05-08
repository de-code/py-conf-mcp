from pathlib import Path

import yaml

from py_conf_mcp.config import (
    FromPythonClassConfig,
    ServerConfig,
    AppConfig,
    EnvironmentVariables,
    FromPythonFunctionConfig,
    ToolDefinitionsConfig,
    load_app_config
)
from py_conf_mcp.config_typing import (
    FromPythonClassConfigDict,
    ServerConfigDict,
    AppConfigDict,
    FromPythonFunctionConfigDict,
    ToolDefinitionsConfigDict
)


FROM_PYTHON_FUNCTION_CONFIG_DICT_1: FromPythonFunctionConfigDict = {
    'name': 'tool_1',
    'module': 'tool_module_1',
    'key': 'tool_key_1'
}


FROM_PYTHON_CLASS_CONFIG_DICT_1: FromPythonClassConfigDict = {
    'name': 'tool_1',
    'module': 'tool_module_1',
    'className': 'tool_class_1'
}


TOOL_DEFINITIONS_CONFIG_DICT_1: ToolDefinitionsConfigDict = {
    'fromPythonFunction': [
        FROM_PYTHON_FUNCTION_CONFIG_DICT_1
    ]
}


SERVER_CONFIG_DICT_1: ServerConfigDict = {
    'name': 'Test MCP Server',
    'tools': ['tool_1', 'tool_2']
}


APP_CONFIG_DICT_1: AppConfigDict = {
    'server': SERVER_CONFIG_DICT_1
}


class TestFromPythonFunctionConfig:
    def test_should_load_tool_config(self):
        tool_config = FromPythonFunctionConfig.from_dict(
            FROM_PYTHON_FUNCTION_CONFIG_DICT_1
        )
        assert tool_config.name == FROM_PYTHON_FUNCTION_CONFIG_DICT_1['name']
        assert tool_config.module == FROM_PYTHON_FUNCTION_CONFIG_DICT_1['module']
        assert tool_config.key == FROM_PYTHON_FUNCTION_CONFIG_DICT_1['key']

    def test_should_load_tool_description(self):
        tool_config = FromPythonFunctionConfig.from_dict({
            **FROM_PYTHON_FUNCTION_CONFIG_DICT_1,
            'description': 'Description 1'
        })
        assert tool_config.description == 'Description 1'


class TestFromPythonClassConfig:
    def test_should_load_tool_config(self):
        tool_config = FromPythonClassConfig.from_dict(
            FROM_PYTHON_CLASS_CONFIG_DICT_1
        )
        assert tool_config.name == FROM_PYTHON_CLASS_CONFIG_DICT_1['name']
        assert tool_config.module == FROM_PYTHON_CLASS_CONFIG_DICT_1['module']
        assert tool_config.class_name == FROM_PYTHON_CLASS_CONFIG_DICT_1['className']
        assert tool_config.init_parameters == {}

    def test_should_load_description(self):
        tool_config = FromPythonClassConfig.from_dict({
            **FROM_PYTHON_CLASS_CONFIG_DICT_1,
            'description': 'Description 1'
        })
        assert tool_config.description == 'Description 1'

    def test_should_load_init_parameters(self):
        tool_config = FromPythonClassConfig.from_dict({
            **FROM_PYTHON_CLASS_CONFIG_DICT_1,
            'initParameters': {
                'param_1': 'value_1'
            }
        })
        assert tool_config.init_parameters == {
            'param_1': 'value_1'
        }


class TestToolDefinitionsConfig:
    def test_should_be_falsy_if_empty(self):
        tool_config = ToolDefinitionsConfig.from_dict({
        })
        assert bool(tool_config) is False

    def test_should_load_tool_config_from_python_function(self):
        tool_config = ToolDefinitionsConfig.from_dict({
            'fromPythonFunction': [
                FROM_PYTHON_FUNCTION_CONFIG_DICT_1
            ]
        })
        assert tool_config.from_python_function == [
            FromPythonFunctionConfig.from_dict(
                FROM_PYTHON_FUNCTION_CONFIG_DICT_1
            )
        ]
        assert bool(tool_config) is True

    def test_should_load_tool_config_from_python_class(self):
        tool_config = ToolDefinitionsConfig.from_dict({
            'fromPythonClass': [
                FROM_PYTHON_CLASS_CONFIG_DICT_1
            ]
        })
        assert tool_config.from_python_class == [
            FromPythonClassConfig.from_dict(
                FROM_PYTHON_CLASS_CONFIG_DICT_1
            )
        ]
        assert bool(tool_config) is True


class TestServerConfig:
    def test_should_load_name(self):
        agent_config = ServerConfig.from_dict(SERVER_CONFIG_DICT_1)
        assert agent_config.name == SERVER_CONFIG_DICT_1['name']

    def test_should_load_tools(self):
        agent_config = ServerConfig.from_dict(SERVER_CONFIG_DICT_1)
        assert agent_config.tools == SERVER_CONFIG_DICT_1['tools']


class TestAppConfig:
    def test_should_load_server_config(self):
        app_config = AppConfig.from_dict(APP_CONFIG_DICT_1)
        assert app_config.server == ServerConfig.from_dict(APP_CONFIG_DICT_1['server'])

    def test_should_load_tool_definitions(self):
        app_config = AppConfig.from_dict({
            **APP_CONFIG_DICT_1,
            'toolDefinitions': TOOL_DEFINITIONS_CONFIG_DICT_1
        })
        assert app_config.tool_definitions == ToolDefinitionsConfig.from_dict(
            TOOL_DEFINITIONS_CONFIG_DICT_1
        )


class TestLoadAppConfig:
    def test_should_load_app_config_from_file(self, mock_env: dict, tmp_path: Path):
        config_file = tmp_path / 'config.yaml'
        config_file.write_text(yaml.safe_dump(APP_CONFIG_DICT_1), encoding='utf-8')
        mock_env[EnvironmentVariables.CONFIG_FILE] = str(config_file)
        app_config = load_app_config()
        assert app_config == AppConfig.from_dict(APP_CONFIG_DICT_1)
