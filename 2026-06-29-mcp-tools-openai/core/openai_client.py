from openai import OpenAI

class OpenAiClient:
    def __init__(self, model: str):
        self.client = OpenAI()
        self.model = model

    def add_user_message(self, messages: list, message):
        if hasattr(message, "content"):
            content = message.content
        else:
            content = message
            
        messages.append({
            "role": "user",
            "content": content,
        })

    def add_assistant_message(self, messages: list, message):
        if isinstance(message, dict):
            messages.append(message)
        elif hasattr(message, "content"):
            msg_dict = {
                "role": "assistant",
                "content": message.content,
            }
            if hasattr(message, "tool_calls") and message.tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in message.tool_calls
                ]
            messages.append(msg_dict)
        else:
            messages.append({
                "role": "assistant",
                "content": str(message),
            })

    def text_from_message(self, message) -> str:
        if hasattr(message, "content"):
            return message.content or ""
        elif isinstance(message, dict):
            return message.get("content") or ""
        return str(message)

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
    ):
        openai_messages = []
        if system:
            openai_messages.append({"role": "system", "content": system})
        openai_messages.extend(messages)

        params = {
            "model": self.model,
            "messages": openai_messages,
            "temperature": temperature,
        }
        if stop_sequences:
            params["stop"] = stop_sequences

        if tools:
            openai_tools = []
            for tool in tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool["input_schema"]
                    }
                })
            params["tools"] = openai_tools

        response = self.client.chat.completions.create(**params)
        return response.choices[0].message
