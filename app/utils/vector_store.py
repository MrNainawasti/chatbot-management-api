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

def search_vector_store(query_text: str, chatbot_id: int, top_k: int = 3) -> list[str]:
    """
    Searches ChromaDB for the top K most relevant text chunks matching the query
    for a specific chatbot.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
        where={"chatbot_id": chatbot_id}
    )
    if results and "documents" in results and results["documents"]:
        return results["documents"][0]

    return []
       


