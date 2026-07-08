from sqlalchemy.orm import Session
from models.user import User
from models.conversation import Conversation
from models.message import Message


#  User 

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, hashed_password: str, role: str = "user") -> User:
    user = User(email=email, hashed_password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


#  Conversation 

def get_conversations(db: Session, user_id: int) -> list[Conversation]:
    return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.created_at.desc()).all()

def get_conversation(db: Session, conversation_id: int) -> Conversation | None:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def create_conversation(db: Session, user_id: int, title: str = "New Chat") -> Conversation:
    convo = Conversation(user_id=user_id, title=title)
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return convo

def delete_conversation(db: Session, conversation_id: int) -> None:
    convo = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if convo:
        db.delete(convo)
        db.commit()


#  Message 

def get_messages(db: Session, conversation_id: int) -> list[Message]:
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()

def create_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
