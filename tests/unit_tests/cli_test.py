import pytest

from py_conf_mcp.cli import create_mcp_for_app_config
from py_conf_mcp.config import (
    AppConfig,
    FromPythonClassConfig,
    FromPythonFunctionConfig,
    ServerConfig,
    ToolDefinitionsConfig
)


FROM_PYTHON_FUNCTION_CONFIG_1 = FromPythonFunctionConfig(
    name='tool_1',
    module='py_conf_mcp.tools.example.joke',
    key='get_joke'
)


FROM_PYTHON_CLASS_CONFIG_1 = FromPythonClassConfig(
    name='get_static_content',
    module='py_conf_mcp.tools.sources.static',
    class_name='StaticContentTool',
    init_parameters={
        'content': 'Static content'
    }
)


class TestCreateMcpForAppConfig:
    @pytest.mark.asyncio
    async def test_should_create_mcp_with_tools_from_function(self):
        mcp = create_mcp_for_app_config(app_config=AppConfig(
            tool_definitions=ToolDefinitionsConfig(
                from_python_function=[FROM_PYTHON_FUNCTION_CONFIG_1]
            ),
            server=ServerConfig(
                name='Test MCP Server',
                tools=[FROM_PYTHON_FUNCTION_CONFIG_1.name]
            )
        ))
        assert mcp.name == 'Test MCP Server'
        tools = await mcp.get_tools()
        assert tools

    @pytest.mark.asyncio
    async def test_should_create_mcp_with_tools_from_class(self):
        mcp = create_mcp_for_app_config(app_config=AppConfig(
            tool_definitions=ToolDefinitionsConfig(
                from_python_class=[FROM_PYTHON_CLASS_CONFIG_1]
            ),
            server=ServerConfig(
                name='Test MCP Server',
                tools=[FROM_PYTHON_CLASS_CONFIG_1.name]
            )
        ))
        assert mcp.name == 'Test MCP Server'
        tools = await mcp.get_tools()
        assert tools
