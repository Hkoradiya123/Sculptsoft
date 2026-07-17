from prompt_toolkit import PromptSession
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
import halo

from core import init_components, fresh_messages, get_context_window
from file_completer import PROJECT_ROOT

import os, re
from prompt_toolkit.completion import Completer, Completion

MAX_TOOL_ROUNDS = 5

def _list_project_files(root):
    IGNORED = {".git", ".venv", "venv", "__pycache__", "node_modules", "chroma_db", ".idea", ".vscode"}
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED]
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace("\\", "/")
            files.append(rel)
    return files

class FileMentionCompleter(Completer):
    def __init__(self, root):
        self.root = root
        self.files = _list_project_files(root)
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        match = re.search(r"@([^\s@]*)$", text)
        if not match:
            return
        typed = match.group(1).lower()
        for path in self.files:
            if typed in path.lower():
                yield Completion(path, start_position=-len(typed), display=path)

indexed_files = set()
completer = FileMentionCompleter(PROJECT_ROOT)
model_with_tools, tools_by_name, _ = init_components(
    indexed_files,
    warn_callback=lambda msg: print(f"\n[Warning] {msg}")
)

session = PromptSession(completer=completer, complete_while_typing=True)
messages = fresh_messages()



os.system('cls' if os.name == 'nt' else 'clear')
while True:
    try:
        query = session.prompt("\nUser : ")
        if query.lower() == "exit":
            break

        messages.append(HumanMessage(content=query))
        spinner = halo.Halo(text="Thinking...")
        spinner.start()

        ai_msg = model_with_tools.invoke(get_context_window(messages))
        spinner.stop()
        messages.append(ai_msg)

        rounds = 0
        while ai_msg.tool_calls and rounds < MAX_TOOL_ROUNDS:
            for call in ai_msg.tool_calls:
                result = tools_by_name[call["name"]].invoke(call["args"])
                messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
            ai_msg = model_with_tools.invoke(get_context_window(messages))
            messages.append(ai_msg)
            rounds += 1

        # Stream final response
        messages.pop()
        print("\nAI : ", end="", flush=True)
        reply_chunks = []
        for chunk in model_with_tools.stream(get_context_window(messages)):
            if chunk.content:
                print(chunk.content, end="", flush=True)
                reply_chunks.append(chunk.content)
        print()
        messages.append(AIMessage(content="".join(reply_chunks)))

    except KeyboardInterrupt:
        print("\nExiting.")
        break
    except Exception as e:
        print(f"\nError: {e}")
