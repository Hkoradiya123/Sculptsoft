from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api.deps import get_db, get_current_user
from schemas.message import Message
from services.message_service import list_messages, add_message

router = APIRouter()


class MessageCreate(BaseModel):
    role: str = Field(default="user", pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


@router.get("/{conversation_id}", response_model=list[Message])
def get_messages_route(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_messages(db, conversation_id, current_user.id)


@router.post("/{conversation_id}", response_model=Message, status_code=201)
def create_message_route(
    conversation_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return add_message(db, conversation_id, payload.role, payload.content)
