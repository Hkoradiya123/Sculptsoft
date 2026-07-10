from sqlalchemy.orm import Session

from database.crud import get_user_by_email, create_user
from core.security import hash_password, verify_password, create_access_token, create_refresh_token
from core.exceptions import UnauthorizedException, ConflictException
from schemas.auth import RegisterRequest, LoginRequest, LoginResponse


def register(db: Session, payload: RegisterRequest) -> dict:
    if get_user_by_email(db, payload.email):
        raise ConflictException("Email already registered")
    create_user(db, payload.email, hash_password(payload.password), payload.role)
    return {"detail": "Registered successfully"}


def login(db: Session, payload: LoginRequest) -> LoginResponse:
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise UnauthorizedException("Invalid credentials")
    data = {"sub": str(user.id), "role": user.role}
    return LoginResponse(
        access_token=create_access_token(data),
        refresh_token=create_refresh_token(data),
        token_type="bearer",
    )
