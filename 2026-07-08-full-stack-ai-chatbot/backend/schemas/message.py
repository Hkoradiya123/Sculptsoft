from pydantic import BaseModel, EmailStr, Field

class Message(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str

    class Config:
        orm_mode = True