from pydantic import BaseModel, EmailStr, Field

class Conversation(BaseModel):
    id: int
    title: str
    user_id: int

    class Config:
        orm_mode = True