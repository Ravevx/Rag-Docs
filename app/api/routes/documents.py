from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.azure_clients import get_blob_client
from app.rag.chunker import extract_text_from_pdf, extract_text_from_markdown, chunk_text
from app.rag.indexer import index_chunks
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()

ALLOWED_EXTENSIONS = [".pdf", ".md", ".txt"]


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Only PDF, MD, and TXT files are supported")

    file_bytes = await file.read()

    # Upload to Azure Blob Storage
    blob_client = get_blob_client()
    container_client = blob_client.get_container_client(settings.azure_storage_container_name)
    try:
        container_client.create_container()
    except Exception:
        pass

    container_client.upload_blob(name=file.filename, data=file_bytes, overwrite=True)

    # Extract text based on file type
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    else:
        text = extract_text_from_markdown(file_bytes)

    # Chunk and index
    chunks = chunk_text(text)
    index_chunks(chunks, file.filename)

    return {
        "message": "Document uploaded and indexed successfully",
        "filename": file.filename,
        "chunks_indexed": len(chunks)
    }


@router.get("/list")
async def list_documents():
    blob_client = get_blob_client()
    container_client = blob_client.get_container_client(settings.azure_storage_container_name)
    try:
        blobs = [blob.name for blob in container_client.list_blobs()]
        return {"documents": blobs}
    except Exception:
        return {"documents": []}