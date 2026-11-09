from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas
from .dependencies import require_teacher

router = APIRouter(prefix="/pms/users", tags=["PMS Users"])


# TEACHER: GET all users
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_teacher)
):
    return db.query(models.User).all()


# TEACHER: GET user by ID with their tasks
@router.get("/{user_id}", response_model=schemas.UserWithTasks)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_teacher)
):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

