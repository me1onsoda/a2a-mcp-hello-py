"""A2A Agent that uses Weather MCP Server."""
from mcp_client import MCPWeatherClient

class WeatherMCPAgent:
    def __init__(self, mcp_url: str):
        self.mcp_client = MCPWeatherClient(mcp_url)

    async def invoke(self, user_message: str) -> str:
        return await self.mcp_client.get_weather(user_message.strip())