from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import documents, chat
from app.core.config import get_settings
from app.rag.indexer import create_index


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    description="Enterprise RAG system built on Azure AI Search + OpenAI",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])


@app.on_event("startup")
async def startup_event():
    create_index()


@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "status": "running",
        "env": settings.app_env
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}