from pydantic import BaseModel
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str

class DocumentCreate(DocumentBase):
    file_path: str

class DocumentResponse(DocumentBase):
    id: int
    chatbot_id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

