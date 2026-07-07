from sqlalchemy.orm import Session
from database.db import SessionLocal, Conversation, Message


def get_db() -> Session:
    return SessionLocal()


def get_all_conversations(db: Session) -> list[Conversation]:
    return db.query(Conversation).order_by(Conversation.created_at.desc()).all()


def get_conversation(db: Session, conversation_id: int) -> Conversation | None:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()


def create_conversation(db: Session, title: str = "New Chat") -> Conversation:
    convo = Conversation(title=title)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return convo


def update_conversation_title(db: Session, conversation_id: int, title: str) -> None:
    db.query(Conversation).filter(Conversation.id == conversation_id).update({"title": title})
    db.commit()


def get_messages(db: Session, conversation_id: int) -> list[Message]:
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.id)
        .all()
    )


def save_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
