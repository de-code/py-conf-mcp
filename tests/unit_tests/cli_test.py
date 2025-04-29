import pytest

from py_conf_mcp.cli import create_mcp_for_app_config
from py_conf_mcp.config import (
    AppConfig,
    FromPythonFunctionConfig,
    ServerConfig,
    ToolDefinitionsConfig
)


class TestCreateMcpForAppConfig:
    @pytest.mark.asyncio
    async def test_should_create_mcp_with_tools(self):
        mcp = create_mcp_for_app_config(app_config=AppConfig(
            tool_definitions=ToolDefinitionsConfig(
                from_python_function=[
                    FromPythonFunctionConfig(
                        name='tool_1',
                        module='py_conf_mcp.tools.example.joke',
                        key='get_joke'
                    )
                ]
            ),
            server=ServerConfig(
                tools=['tool_1']
            )
        ))
        tools = await mcp.get_tools()
        assert tools
