from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api.deps import get_db, get_current_user
from services.message_service import list_messages, add_message
from services.openai_service import chat, chat_stream
from database.crud import get_conversation
from core.exceptions import NotFoundException, ForbiddenException

router = APIRouter()


class ChatRequest(BaseModel):
    content: str = Field(..., min_length=1)
    model: str = Field(default="gpt-4o")


@router.post("/{conversation_id}")
def chat_route(
    conversation_id: int,
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    convo = get_conversation(db, conversation_id)
    if not convo:
        raise NotFoundException("Conversation not found")
    if convo.user_id != current_user.id:
        raise ForbiddenException()

    add_message(db, conversation_id, "user", payload.content)

    history = [
        {"role": m.role, "content": m.content}
        for m in list_messages(db, conversation_id, current_user.id)
    ]

    reply = chat(history, model=payload.model)
    add_message(db, conversation_id, "assistant", reply)

    return {"role": "assistant", "content": reply}


@router.post("/{conversation_id}/stream")
def chat_stream_route(
    conversation_id: int,
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    convo = get_conversation(db, conversation_id)
    if not convo:
        raise NotFoundException("Conversation not found")
    if convo.user_id != current_user.id:
        raise ForbiddenException()

    add_message(db, conversation_id, "user", payload.content)

    history = [
        {"role": m.role, "content": m.content}
        for m in list_messages(db, conversation_id, current_user.id)
    ]

    collected = []

    def generate():
        for chunk in chat_stream(history, model=payload.model):
            collected.append(chunk)
            yield chunk
        add_message(db, conversation_id, "assistant", "".join(collected))

    return StreamingResponse(generate(), media_type="text/plain")
