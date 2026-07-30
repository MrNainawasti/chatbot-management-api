from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.chatbot import ChatBotCreate, ChatBotUpdate, ChatBotResponse
from app.repositories import chatbot as chatbot_repo
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ChatBotResponse)
def create_chatbot(
    chatbot: ChatBotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # check if user already has the bot with exactly same name
    existing_bot = chatbot_repo.get_chatbot_by_name(db=db, owner_id=current_user.id, name=chatbot.name)
    if existing_bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chatbot already exists."
        )

    return chatbot_repo.create_chatbot(db=db, chatbot=chatbot, owner_id=current_user.id)

@router.get("/", response_model=List[ChatBotResponse])
def get_my_chatbots(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return chatbot_repo.get_chatbots_by_user(db=db, owner_id=current_user.id, skip=skip, limit=limit)

@router.get("/{chatbot_id}", response_model=ChatBotResponse)
def get_single_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chatbot = chatbot_repo.get_chatbot(db=db, chatbot_id=chatbot_id, owner_id=current_user.id)
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    return chatbot

@router.put("/{chatbot_id}", response_model=ChatBotResponse)
def update_chatbot(
    chatbot_id: int,
    chatbot_update: ChatBotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chatbot = chatbot_repo.update_chatbot(
        db=db, chatbot_id=chatbot_id, owner_id=current_user.id, chatbot_update=chatbot_update
    )
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    return chatbot

@router.delete("/{chatbot_id}")
def delete_chatbot(
    chatbot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = chatbot_repo.delete_chatbot(
        db=db, chatbot_id=chatbot_id, owner_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found"
        )
    return {"message": "Chatbot deleted successfully"}


