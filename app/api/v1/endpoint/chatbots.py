from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.chatbot import ChatBotCreate, ChatBotUpdate, ChatBotResponse
from app.schemas.chat import ChatRequest, ChatResponse
from app.repositories import chatbot as chatbot_repo
from app.api.dependencies import get_current_user
from app.models.user import User
from app.utils.vector_store import search_vector_store
from app.utils.llm import generate_ai_response

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

@router.post("/{chatbot_id}/chat", response_model=ChatResponse)
async def chat_with_bot(
    chatbot_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # verify if chatbot exists and belongs to the user
    chatbot = chatbot_repo.get_chatbot(db=db, chatbot_id=chatbot_id, owner_id=current_user.id)
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="chatbot not found"
        )

    # search chromaDB for relevant chunks
    relevant_chunks = search_vector_store(
        query_text=request.message,
        chatbot_id=chatbot_id,
        top_k=3
    )

    # combine retrieved chunks into context string
    content_text = "\n\n".join(relevant_chunks) if relevant_chunks else "No specific document context found."

    # construct system prompt
    constructed_prompt = (
        f"You are an AI assistant named '{chatbot.name}'. {chatbot.system_prompt}\n\n"
        f"Use the following document context to answer the user's question:\n"
        f"If the context does not contain the answer, state clearly that you do not know based on the documents.\n\n"
        f"---CONTEXT---\n{content_text}\n-----------------\n"
        f"User Question: {request.message}"
    )

    ai_answer = generate_ai_response(prompt=constructed_prompt)
   
    return ChatResponse(
        answer= ai_answer,
        sources=relevant_chunks
    )