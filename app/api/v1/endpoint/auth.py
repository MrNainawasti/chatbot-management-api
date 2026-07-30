from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.repositories import user as user_repo
from app.core import security

router = APIRouter()

@router.post("/login",)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_repo.get_user_by_email(db, email=form_data.username)

    # verify user exists and password is correct
    if not user or not security.verify_password(form_data.password, user.hashed_password):  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # create JWT token
    access_token = security.create_accesss_token(data={"sub": user.email})

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }
            