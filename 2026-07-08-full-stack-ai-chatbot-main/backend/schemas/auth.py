from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=72)
    role: str = "user"

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=72)

class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str  = Field(..., description="JWT refresh token")
    token_type: str = Field(..., description="Type of the token, usually 'bearer'"),
class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of the token, usually 'bearer'")
    
class ResetPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    new_password: str = Field(..., min_length=6, max_length=72)
    reset_token: str = Field(..., description="Token sent to the user's email for password reset")
    
