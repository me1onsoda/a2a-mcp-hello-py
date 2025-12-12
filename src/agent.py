"""A2A Agent that uses Groq (Llama 3) and MCP."""
import os
import json
from openai import OpenAI
from mcp_client import MCPWeatherClient

class WeatherMCPAgent:
    def __init__(self, mcp_url: str):
        self.mcp_client = MCPWeatherClient(mcp_url)
        
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY")
        )

    async def invoke(self, user_message: str) -> str:
        """
        사용자 메시지 -> Groq(생각) -> 도구 실행 여부 판단 -> (필요시) MCP 호출 -> 최종 답변
        """
        system_prompt = """
        당신은 'SBK 날씨 비서'입니다. 한국어로 대화하며, 항상 친절하고 활기찬 톤을 유지하세요.
        
        [지시사항]
        1. 사용자가 지역 날씨를 물어보면, 반드시 제공된 'get_weather' 도구를 사용하세요.
        2. 도구의 결과(기온, 강수량 등)를 보고, 옷차림이나 우산 필요 여부를 조언해 주세요.
        3. 날씨와 관련 없는 질문에는 "죄송하지만 저는 날씨 정보만 알 수 있습니다."라고 정중히 거절하세요.
        """

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "특정 지역의 현재 날씨 정보를 조회합니다.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "region": {
                                "type": "string",
                                "description": "날씨를 조회할 지역 이름 (예: 서울, 부산, 제주)",
                            }
                        },
                        "required": ["region"],
                    },
                },
            }
        ]
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=messages,
                tools=tools,
                tool_choice="auto", 
            )
        except Exception as e:
            return f"Groq 연결 오류가 발생했습니다: {str(e)}"

        response_message = response.choices[0].message

        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            
            try:
                function_args = json.loads(tool_call.function.arguments)
                region = function_args.get("region", "서울") 
            except:
                region = "서울"

            if function_name == "get_weather":
                weather_data = await self.mcp_client.get_weather(region)
                
                messages.append(response_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(weather_data),
                })

                final_response = self.client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=messages,
                )
                
                return final_response.choices[0].message.content
        
        return response_message.content
