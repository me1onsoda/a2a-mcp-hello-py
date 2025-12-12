"""MCP Client for calling Weather Server."""
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

class MCPWeatherClient:
    def __init__(self, mcp_url: str):
        self.mcp_url = mcp_url

    async def get_weather(self, region: str) -> str:
        """Call the get_weather tool on MCP server."""
        async with streamablehttp_client(self.mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "get_weather",
                    arguments={"region": region}
                )

                if result.content and len(result.content) > 0:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        return content.text
                return "날씨 정보를 가져오지 못했습니다."