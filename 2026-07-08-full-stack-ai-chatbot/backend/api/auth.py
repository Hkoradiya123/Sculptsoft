from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.auth import RegisterRequest, LoginRequest, LoginResponse
from core.security import create_access_token, create_refresh_token, hash_password, verify_password
from database.crud import get_user_by_email, create_user
from api.deps import get_db
from core.exceptions import UnauthorizedException, ConflictException

router = APIRouter()


@router.post("/register", status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if get_user_by_email(db, payload.email):
        raise ConflictException("Email already registered")
    create_user(db, payload.email, hash_password(payload.password), payload.role)
    return {"detail": "Registered successfully"}


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise UnauthorizedException("Invalid credentials")
    data = {"sub": str(user.id), "role": user.role}
    return LoginResponse(
        access_token=create_access_token(data),
        refresh_token=create_refresh_token(data),
        token_type="bearer",
    )
