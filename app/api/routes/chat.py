from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.rag.retriever import search_documents
from app.rag.generator import generate_answer


router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    top_k: int = 5


class ChatResponse(BaseModel):
    answer: str
    sources: list


@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    chunks = search_documents(request.question, top_k=request.top_k)

    if not chunks:
        return ChatResponse(
            answer="No relevant documents found. Please upload documents first.",
            sources=[]
        )

    answer = generate_answer(request.question, chunks)

    return ChatResponse(answer=answer, sources=[])