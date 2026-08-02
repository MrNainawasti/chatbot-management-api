import chromadb
from chromadb.config import Settings

# initialize a persistent client that saves data to a local folder
CHROMA_DATA_PATH = "chroma_data"
chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

collection = chroma_client.get_or_create_collection(name="chatbot_knowledge_base")

def add_chunk_to_vector_store(chunks: list[str], chatbot_id: int, document_id: int):
    if not chunks:
        return

    ids = []
    metadatas = []

    for i, _ in enumerate(chunks):
        ids.append(f"bot_{chatbot_id}_doc_{document_id}_chunk_{i}")


        metadatas.append({
            "chatbot_id": chatbot_id,
            "document_id": document_id,
            "chunks": i
        })

    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )




