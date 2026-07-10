from sqlalchemy.orm import Session

from database.crud import get_user_by_id, get_user_by_email
from core.exceptions import NotFoundException


def get_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise NotFoundException("User not found")
    return user
