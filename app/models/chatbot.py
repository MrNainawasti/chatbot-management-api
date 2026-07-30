from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class ChatBot(Base):
    __tablename__ = "chatbots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    color_theme = Column(String, default="#000000")
    model_type = Column(String, default="gpt-3.5-turbo")
    system_prompt = Column(String, default="Hey there!")

    # foreign key
    owner_id = Column(Integer, ForeignKey("users.id"))

    # linking chatbots with user
    owner = relationship("User", back_populates="chatbots")

