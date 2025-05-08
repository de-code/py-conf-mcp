from py_conf_mcp.tools.sources.static import StaticContentTool


class TestStaticContentTool:
    def test_should_return_provided_content(self):
        tool = StaticContentTool(
            content='content_1'
        )
        assert tool() == 'content_1'
