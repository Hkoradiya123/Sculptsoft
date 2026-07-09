from sqlalchemy.orm import Session

from database.crud import get_messages, create_message, get_conversation
from core.exceptions import NotFoundException, ForbiddenException


def list_messages(db: Session, conversation_id: int, user_id: int):
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise NotFoundException("Conversation not found")
    if conversation.user_id != user_id:
        raise ForbiddenException("Not your conversation")
    return get_messages(db, conversation_id)


def add_message(db: Session, conversation_id: int, role: str, content: str):
    return create_message(db, conversation_id, role, content)
