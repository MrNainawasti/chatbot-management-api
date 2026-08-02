def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        # avoid empty strings or trailing whitespace chunks
        if chunk.strip():
            chunks.append(chunk.strip())

        start += (chunk_size - overlap)

    return chunks


