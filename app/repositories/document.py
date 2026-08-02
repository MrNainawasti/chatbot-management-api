from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document import DocumentCreate

def create_document(db: Session, document: DocumentCreate, chatbot_id: int):
    db_document = Document(
        filename = document.filename,
        file_path = document.file_path,
        chatbot_id = chatbot_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document_by_chatbot(db: Session, chatbot_id: int):
    return db.query(Document).filter(Document.chatbot_id == chatbot_id).all()