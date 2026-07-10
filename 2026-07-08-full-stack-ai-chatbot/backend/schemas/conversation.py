from pydantic import BaseModel, Field
from datetime import datetime


class ConversationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class ConversationUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class ConversationRead(BaseModel):
    id: int
    title: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
