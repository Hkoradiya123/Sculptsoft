import json
from datetime import datetime

from .db import Base, Conversation, Message, SessionLocal, engine


def get_db():
    Base.metadata.create_all(bind=engine)
    return SessionLocal()


def get_all_conversations(db):
    return db.query(Conversation).order_by(Conversation.created_at.desc()).all()


def create_conversation(db, title: str) -> Conversation:
    convo = Conversation(title=title, created_at=datetime.utcnow())
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return convo


def update_conversation_title(db, conversation_id: int, title: str) -> None:
    db.query(Conversation).filter(Conversation.id == conversation_id).update({"title": title})
    db.commit()


def get_messages(db, conversation_id: int):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )


def save_message(db, conversation_id: int, role: str, content: str, trace: list[dict] | None = None) -> Message:
    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        tool_trace=json.dumps(trace) if trace else None,
        created_at=datetime.utcnow(),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
