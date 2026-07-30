from sqlalchemy.orm import Session
from app.models.chatbot import ChatBot
from app.schemas.chatbot import ChatBotCreate, ChatBotUpdate

def create_chatbot(db: Session, chatbot: ChatBotCreate, owner_id: int):
    db_chatbot = ChatBot(**chatbot.model_dump(), owner_id= owner_id)
    db.add(db_chatbot)
    db.commit()
    db.refresh(db_chatbot)
    return db_chatbot

def get_chatbot_by_name(db: Session, owner_id: int, name: str):
    return db.query(ChatBot).filter(
        ChatBot.owner_id == owner_id, 
        ChatBot.name == name
    ).first()


def get_chatbots_by_user(db: Session, owner_id: int, skip: int = 0, limit:int = 100):
    return db.query(ChatBot).filter(ChatBot.owner_id == owner_id).offset(skip).limit(limit).all()

def get_chatbot(db: Session, chatbot_id: int, owner_id: int):
    return db.query(ChatBot).filter(
        ChatBot.id == chatbot_id,
        ChatBot.owner_id == owner_id
        ).first()

def update_chatbot(db:Session, chatbot_id: int, owner_id: int, chatbot_update: ChatBotUpdate):
    db_chatbot = get_chatbot(db, chatbot_id, owner_id)
    if not db_chatbot:
        return None

    update_data = chatbot_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_chatbot, key, value)

    db.commit()
    db.refresh(db_chatbot)

    return db_chatbot

def delete_chatbot(db: Session, chatbot_id: int, owner_id: int):
    db_chatbot = get_chatbot(db, chatbot_id, owner_id)
    if not db_chatbot:
        return False

    db.delete(db_chatbot)
    db.commit()
    return True