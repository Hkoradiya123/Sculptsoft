from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_db, get_current_user
from schemas.conversation import ConversationCreate, ConversationUpdate, ConversationRead
from services.conversation_service import list_conversations, remove_conversation
from database.crud import create_conversation, get_conversation, get_conversations
from core.exceptions import NotFoundException, ForbiddenException

router = APIRouter()


@router.get("", response_model=list[ConversationRead])
def get_conversations_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_conversations(db, current_user.id)


@router.post("", response_model=ConversationRead, status_code=201)
def create_conversation_route(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_conversation(db, current_user.id, payload.title)


@router.get("/{conversation_id}", response_model=ConversationRead)
def get_conversation_route(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    convo = get_conversation(db, conversation_id)
    if not convo:
        raise NotFoundException("Conversation not found")
    if convo.user_id != current_user.id:
        raise ForbiddenException()
    return convo


@router.put("/{conversation_id}", response_model=ConversationRead)
def update_conversation_route(
    conversation_id: int,
    payload: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    convo = get_conversation(db, conversation_id)
    if not convo:
        raise NotFoundException("Conversation not found")
    if convo.user_id != current_user.id:
        raise ForbiddenException()
    convo.title = payload.title
    db.commit()
    db.refresh(convo)
    return convo


@router.delete("/{conversation_id}", status_code=204)
def delete_conversation_route(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    remove_conversation(db, conversation_id, current_user.id)
