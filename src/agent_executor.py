"""A2A Agent Executor for Hello MCP Agent."""

from a2a.server.agent_execution import AgentExecutor, RequestContext  # type: ignore
from a2a.server.events import EventQueue  # type: ignore
from a2a.server.tasks import TaskUpdater  # type: ignore
from a2a.types import Part, TaskState, TextPart  # type: ignore
from a2a.utils import new_agent_text_message, new_task  # type: ignore
from agent import WeatherMCPAgent  # type: ignore


class WeatherMCPAgentExecutor(AgentExecutor):
    def __init__(self, mcp_url: str):
        self.agent = WeatherMCPAgent(mcp_url)

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        user_message = context.get_user_input() if hasattr(context, 'get_user_input') else ""
        if not user_message and context.message and context.message.parts:
            for part in context.message.parts:
                if hasattr(part, 'text'):
                    user_message = part.text
                    break
                elif hasattr(part, 'root') and hasattr(part.root, 'text'):
                    user_message = part.root.text
                    break

        if not user_message:
            user_message = "서울"

        task = context.current_task or new_task(context.message)
        await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)

        try:
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(f"'{user_message}' 날씨 조회 중...", task.context_id, task.id),
            )

            # 날씨 조회 실행
            result = await self.agent.invoke(user_message)

            await updater.add_artifact([Part(root=TextPart(text=result))], name="weather_info")
            await updater.complete()

        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"오류: {str(e)}", task.context_id, task.id),
                final=True,
            )
            
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("cancel not supported")