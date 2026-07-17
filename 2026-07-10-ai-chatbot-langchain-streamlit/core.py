import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from file_completer import PROJECT_ROOT, _list_project_files
from tools import build_tools

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

SYSTEM_PROMPT = """You are a helpful assistant with access to two tools:
- search_documents: search the already-indexed knowledge base (ChromaDB) by meaning.
- load_file: find and load a specific project file by name (works with or without an '@' prefix), indexing it for future searches.

Use these tools whenever the user asks about a specific file or about content that
might already be indexed. When you use a tool, prefer its results over your own
assumptions for that specific content.

For general questions that aren't about an indexed file or the knowledge base,
answer directly from your own knowledge — do not refuse just because nothing was
retrieved. Only say you don't have enough information if the question clearly
depends on file/document content you searched for and didn't find.
"""


def init_components(indexed_files: set, model_name: str = "gpt-4o", warn_callback=None):
    """Creates and returns (model_with_tools, tools_by_name, vector_store).
    Persists embeddings to disk under chroma_db/ so indexed files survive restarts."""
    persist_dir = str(Path(__file__).parent / "chroma_db")

    vector_store = Chroma(
        persist_directory=persist_dir,
        embedding_function=OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.environ.get("OPENAI_API_KEY"),
        ),
        collection_name="knowledge_base",
    )
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    model = ChatOpenAI(
        model=model_name,
        temperature=0.4,
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    tools, tools_by_name = build_tools(
        vector_store,
        retriever,
        _list_project_files(PROJECT_ROOT),
        indexed_files,
        warn_callback=warn_callback,
    )

    return model.bind_tools(tools), tools_by_name, vector_store


def fresh_messages():
    return [SystemMessage(content=SYSTEM_PROMPT)]


def get_context_window(messages, window: int = 20):
    """Returns SystemMessage + last `window` messages to cap context size."""
    if len(messages) <= window + 1:
        return messages
    return [messages[0]] + messages[-(window):]
