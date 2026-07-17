import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IGNORED_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "chroma_db", ".idea", ".vscode"}


def _list_project_files(root: str) -> list[str]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace("\\", "/")
            files.append(rel)
    return files
