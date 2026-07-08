from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr = Field(description="Valid email address")
    role: str = Field(default="user", description="Role of the user, default is 'user'")


class UserCreate(UserBase):
    email: EmailStr = Field(description="Valid email address")
    password: str = Field(description="Password must be at least 6 characters", min_length=6, max_length=72)


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        