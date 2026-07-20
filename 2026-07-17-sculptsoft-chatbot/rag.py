import os

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "data", "chroma_db")
COLLECTION_NAME = "sculptsoft_site"
EMBEDDING_MODEL = "text-embedding-3-small"

_vectorstore = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
            persist_directory=CHROMA_DIR,
        )
    return _vectorstore


def retrieve(query: str, k: int = 4, fetch_k: int = 20):
    return get_vectorstore().max_marginal_relevance_search(query, k=k, fetch_k=fetch_k)


def format_context(docs) -> str:
    if not docs:
        return ""

    blocks = []
    for doc in docs:
        title = doc.metadata.get("title", "")
        url = doc.metadata.get("url", "")
        blocks.append(f"[{title}]({url})\n{doc.page_content}")

    return "\n\n---\n\n".join(blocks)


def build_rag_context(query: str, k: int = 4) -> str:
    return format_context(retrieve(query, k=k))
