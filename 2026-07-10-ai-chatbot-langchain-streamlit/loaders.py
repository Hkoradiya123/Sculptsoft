import os

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

LOADER_BY_EXTENSION = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
    ".csv": CSVLoader,
    ".docx": Docx2txtLoader,
}

LANGUAGE_BY_EXTENSION = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".ts": Language.TS,
    ".java": Language.JAVA,
    ".go": Language.GO,
    ".cpp": Language.CPP,
    ".c": Language.C,
    ".php": Language.PHP,
    ".rb": Language.RUBY,
    ".rs": Language.RUST,
    ".html": Language.HTML,
    ".md": Language.MARKDOWN,
}

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 120
LARGE_FILE_CHUNK_THRESHOLD = 2000
PREVIEW_CHARS = 1000
MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB — reject before ever reading the file

file_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)


def get_splitter_for(abs_path: str) -> RecursiveCharacterTextSplitter:
    """Returns a language-aware splitter for code/markdown files, else the generic one."""
    ext = os.path.splitext(abs_path)[1].lower()
    language = LANGUAGE_BY_EXTENSION.get(ext)
    if language is None:
        return file_splitter
    return RecursiveCharacterTextSplitter.from_language(
        language=language, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )


def load_file_as_documents(abs_path: str) -> list[Document]:
    """Picks the right loader for a file's extension and loads it into Documents.
    Plain document types use their dedicated loader; any extension registered as a
    programming language falls back to TextLoader, since code is just plain text."""
    ext = os.path.splitext(abs_path)[1].lower()
    loader_cls = LOADER_BY_EXTENSION.get(ext)
    if loader_cls is None:
        if ext in LANGUAGE_BY_EXTENSION:
            loader_cls = TextLoader
        else:
            raise ValueError(f"No loader registered for '{ext}' files")
    return loader_cls(abs_path).load()
