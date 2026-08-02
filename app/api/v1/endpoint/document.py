import os
import shutil
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.repositories import chatbot as chatbot_repo
from app.repositories import document as document_repo
from app.schemas.document import DocumentCreate, DocumentResponse
from app.utils.pdf import extract_text_from_pdf
from app.utils.chunker import chunk_text
from app.utils.vector_store import add_chunk_to_vector_store

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{chatbot_id}/documents", response_model=DocumentResponse)
def upload_document(
    chatbot_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # check if the user actually owns this chatbot
    chatbot = chatbot_repo.get_chatbot(db=db, chatbot_id=chatbot_id, owner_id=current_user.id)
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found!!"
        )
    
    # accepting only pdfs
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )

    # create unique file path
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="couldn't save file!"
        )
    finally:
        file.file.close()

    document_data = DocumentCreate(
        filename=file.filename,
        file_path=file_path
    )

    db_document = document_repo.create_document(db=db, document=document_data, chatbot_id=chatbot_id)

    # extract text
    print(f"Starting to read file {file.filename}...")
    raw_text = extract_text_from_pdf(file_path)

    chunks = chunk_text(raw_text, chunk_size=1000, overlap=150)

    print("Generating embeddings and saving to chromaDB...")
    add_chunk_to_vector_store(
        chunks=chunks,
        chatbot_id=chatbot_id,
        document_id= db_document.id
    )


    return db_document

        
    