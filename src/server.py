"""A2A Server for Weather Agent."""
import os
import uvicorn
from dotenv import load_dotenv
load_dotenv()

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_executor import WeatherMCPAgentExecutor

MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL")
SERVICE_URL = os.environ.get("SERVICE_URL", "")

def create_agent_card(host: str, port: int) -> AgentCard:
    skill = AgentSkill(
        id="korea_weather",
        name="Korea Weather Check",
        description="한국 주요 도시의 날씨를 조회합니다.",
        tags=["weather", "korea", "sbk"],
        examples=["서울", "부산", "제주"],
    )

    if SERVICE_URL:
        agent_url = SERVICE_URL
    else:
        agent_url = f"http://{host}:{port}/"

    return AgentCard(
        name="Korea Weather Agent",
        description="한국 날씨 조회 에이전트입니다.",
        url=agent_url,
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 9999))
    agent_card = create_agent_card(host, port)

    request_handler = DefaultRequestHandler(
        agent_executor=WeatherMCPAgentExecutor(MCP_SERVER_URL),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(agent_card=agent_card, http_handler=request_handler)
    print(f"Starting SBK Weather Agent on {host}:{port}")
    uvicorn.run(server.build(), host=host, port=port)

if __name__ == "__main__":
    main()