import os

from langchain_core.tools import tool

from loaders import (
    get_splitter_for, load_file_as_documents,
    LARGE_FILE_CHUNK_THRESHOLD, PREVIEW_CHARS, MAX_FILE_SIZE_BYTES,
)
from file_completer import PROJECT_ROOT


def build_tools(vector_store, retriever, file_list: list[str], indexed_files: set, warn_callback=None):
    """Builds search_documents and load_file tools as closures over the given
    vector store, retriever, file list, and indexed_files set."""

    @tool
    def search_documents(query: str) -> str:
        """Search the indexed knowledge base (ChromaDB) for content relevant to the query.
        Use this to answer questions about previously indexed documents, PDFs, or code files."""
        results = retriever.invoke(query)
        if not results:
            return "No relevant documents found in the knowledge base."
        return "\n\n".join(doc.page_content for doc in results)

    @tool
    def load_file(file_name: str) -> str:
        """Find a file by name/partial path within the project, OR by a full absolute path
        anywhere on disk, load it, split it, index it into ChromaDB for future searches, and
        return its content. Use this whenever the user references a specific file (with or
        without an '@' prefix, project-relative or a full path) that may not be indexed yet."""
        cleaned = file_name.lstrip("@").strip().strip('"')

        if os.path.isabs(cleaned) and os.path.isfile(cleaned):
            abs_path = cleaned
            rel_path = cleaned
        else:
            matches = [f for f in file_list if cleaned.lower() in f.lower()]
            if not matches:
                return f"No file found matching '{file_name}' in the project."
            rel_path = matches[0]
            abs_path = os.path.join(PROJECT_ROOT, rel_path)

        file_size = os.path.getsize(abs_path)
        if file_size > MAX_FILE_SIZE_BYTES:
            return (
                f"Refused to load '{rel_path}': {file_size / (1024*1024):.1f} MB exceeds the "
                f"{MAX_FILE_SIZE_BYTES / (1024*1024):.0f} MB limit. Not loaded, split, or embedded."
            )

        try:
            docs = load_file_as_documents(abs_path)
        except ValueError as e:
            return f"Cannot load '{rel_path}': {e}"

        splitter = get_splitter_for(abs_path)
        chunks = splitter.split_documents(docs)

        if len(chunks) > LARGE_FILE_CHUNK_THRESHOLD:
            if warn_callback:
                warn_callback(f"'{rel_path}' is large ({len(chunks)} chunks). Indexing anyway.")

        if abs_path not in indexed_files:
            vector_store.add_documents(chunks)
            indexed_files.add(abs_path)

        preview = "\n".join(c.page_content for c in chunks)[:PREVIEW_CHARS]
        return (
            f"Loaded '{rel_path}' — {len(chunks)} chunks indexed into ChromaDB.\n"
            f"Preview (truncated):\n{preview}\n\n"
            f"(Full content is now searchable via search_documents — do not assume this preview is complete.)"
        )

    tools = [search_documents, load_file]
    return tools, {t.name: t for t in tools}
