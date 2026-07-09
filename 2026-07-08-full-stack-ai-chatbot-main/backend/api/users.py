from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_db, get_current_user
from schemas.user import User
from services.user_service import get_user

router = APIRouter()


@router.get("/me", response_model=User)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=User)
def get_user_by_id_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user(db, user_id)
