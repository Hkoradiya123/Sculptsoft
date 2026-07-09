import requests

BASE_URL = "http://localhost:8000"


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def register(email: str, password: str) -> dict:
    r = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    r.raise_for_status()
    return r.json()


def login(email: str, password: str) -> dict:
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    r.raise_for_status()
    return r.json()


def get_conversations(token: str) -> list:
    r = requests.get(f"{BASE_URL}/conversations", headers=_headers(token))
    r.raise_for_status()
    return r.json()


def create_conversation(token: str, title: str) -> dict:
    r = requests.post(f"{BASE_URL}/conversations", json={"title": title}, headers=_headers(token))
    r.raise_for_status()
    return r.json()


def update_conversation(token: str, conversation_id: int, title: str) -> dict:
    r = requests.put(
        f"{BASE_URL}/conversations/{conversation_id}",
        json={"title": title},
        headers=_headers(token),
    )
    r.raise_for_status()
    return r.json()


def delete_conversation(token: str, conversation_id: int) -> None:
    r = requests.delete(
        f"{BASE_URL}/conversations/{conversation_id}",
        headers=_headers(token),
    )
    r.raise_for_status()


def get_messages(token: str, conversation_id: int) -> list:
    r = requests.get(f"{BASE_URL}/messages/{conversation_id}", headers=_headers(token))
    r.raise_for_status()
    return r.json()


def send_message(token: str, conversation_id: int, content: str, model: str = "gpt-4o") -> dict:
    r = requests.post(
        f"{BASE_URL}/chat/{conversation_id}",
        json={"content": content, "model": model},
        headers=_headers(token),
    )
    r.raise_for_status()
    return r.json()


def send_message_stream(token: str, conversation_id: int, content: str, model: str = "gpt-4o"):
    """Yields text chunks from the streaming chat endpoint."""
    with requests.post(
        f"{BASE_URL}/chat/{conversation_id}/stream",
        json={"content": content, "model": model},
        headers=_headers(token),
        stream=True,
    ) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk
