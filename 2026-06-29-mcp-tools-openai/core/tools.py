import json
from typing import Optional, List
from mcp.types import CallToolResult, Tool, TextContent
from mcp_client import MCPClient


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list[Tool]:
        """Gets all tools from the provided clients."""
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in tool_models
            ]
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        """Finds the first client that has the specified tool."""
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, MCPClient], tool_calls
    ) -> List[dict]:
        """Executes a list of tool requests against the provided clients and returns OpenAI tool message dicts."""
        tool_result_blocks: list[dict] = []
        for tool_call in tool_calls:
            tool_use_id = tool_call.id
            tool_name = tool_call.function.name
            
            try:
                tool_input = json.loads(tool_call.function.arguments)
            except Exception as e:
                tool_input = {}

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                tool_result_blocks.append({
                    "role": "tool",
                    "tool_call_id": tool_use_id,
                    "name": tool_name,
                    "content": "Could not find that tool",
                })
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = []
                if tool_output:
                    items = tool_output.content
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list)
                
                tool_result_blocks.append({
                    "role": "tool",
                    "tool_call_id": tool_use_id,
                    "name": tool_name,
                    "content": content_json,
                })
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {e}"
                print(error_message)
                tool_result_blocks.append({
                    "role": "tool",
                    "tool_call_id": tool_use_id,
                    "name": tool_name,
                    "content": json.dumps({"error": error_message}),
                })

        return tool_result_blocks
