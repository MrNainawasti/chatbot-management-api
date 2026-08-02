from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

     # foreign key
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"))

    # linking chatbot with document
    chatbot = relationship("ChatBot", back_populates="documents")

