from core.openai_client import OpenAiClient
from mcp_client import MCPClient
from core.tools import ToolManager


class Chat:
    def __init__(self, openai_service: OpenAiClient, clients: dict[str, MCPClient]):
        self.openai_service: OpenAiClient = openai_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[dict] = []

    async def _process_query(self, query: str) -> bool:
        self.messages.append({"role": "user", "content": query})
        return True

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        should_proceed = await self._process_query(query)
        if not should_proceed:
            return ""

        while True:
            response_message = self.openai_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            self.openai_service.add_assistant_message(self.messages, response_message)

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    print(f"Calling tool: {tool_call.function.name} with arguments: {tool_call.function.arguments}")

                tool_result_parts = await ToolManager.execute_tool_requests(
                    self.clients, response_message.tool_calls
                )

                for result_part in tool_result_parts:
                    self.messages.append(result_part)
            else:
                final_text_response = self.openai_service.text_from_message(
                    response_message
                )
                break

        return final_text_response
