from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.schemas.user import UserResponse, UserCreate
from app.db.database import get_db
from app.repositories import user as user_repo

router = APIRouter()

@router.get("/me")
def get_my_profile(current_token: str = Depends(get_current_user)):
    return {
        "message": "You bypassed the security checkpoint!",
        "token": current_token
    }

@router.post("/register", response_model=UserResponse)
def register_new_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if user already exists
    existing_user = user_repo.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Create the user
    new_user = user_repo.create_user(db=db, user=user)
    return new_user