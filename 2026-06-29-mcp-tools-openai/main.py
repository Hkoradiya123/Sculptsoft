import asyncio
import sys
import os
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.openai_client import OpenAiClient

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv()

# OpenAI Config
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
openai_api_key = os.getenv("OPENAI_API_KEY", "")

assert openai_api_key, "Error: OPENAI_API_KEY cannot be empty. Update .env"


async def main():
    openai_service = OpenAiClient(model=openai_model)

    server_scripts = sys.argv[1:]
    clients = {}

    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_script_path = os.path.join(current_dir, "mcp_server.py")

    command, args = (
        ("uv", ["run", server_script_path])
        if os.getenv("USE_UV", "0") == "1"
        else (sys.executable, [server_script_path])
    )

    print("DEBUG CONFIG:")
    print("sys.executable:", sys.executable)
    print("command:", command)
    print("args:", args)
    print("current_dir:", current_dir)

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(command="uv", args=["run", server_script])
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            openai_service=openai_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()
        
    # Clean up transport/client references and force GC while loop is active to avoid Windows closed loop RuntimeError
    if "client" in locals():
        del client
    del cli, chat, clients, doc_client, stack
    import gc
    gc.collect()
    await asyncio.sleep(0.1)


if __name__ == "__main__":
    if sys.platform == "win32" and sys.version_info < (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
