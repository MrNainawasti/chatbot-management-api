from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(Integer)
    is_active = Column(Boolean, default=True)


    # linking chatbot with owner
    chatbots = relationship("ChatBot", back_populates="owner" )
