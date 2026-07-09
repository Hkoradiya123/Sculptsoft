from sqlalchemy.orm import Session

from database.crud import get_conversations, get_conversation, create_conversation, delete_conversation
from core.exceptions import NotFoundException, ForbiddenException
from services.message_service import add_message


def list_conversations(db: Session, user_id: int):
    return get_conversations(db, user_id)


def new_conversation(db: Session, user_id: int, prompt: str):
    conversation =  create_conversation(db, user_id, prompt)
    id = conversation.id
    add_message(db, id, "user", prompt)
    return conversation




def remove_conversation(db: Session, conversation_id: int, user_id: int):
    conversation = get_conversation(db, conversation_id)
    if not conversation:
        raise NotFoundException("Conversation not found")
    if conversation.user_id != user_id:
        raise ForbiddenException("Not your conversation")
    delete_conversation(db, conversation_id)
