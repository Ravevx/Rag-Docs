from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    app_name: str = "RAG-TASForce"
    app_env: str = "development"

    # Gemini
    gemini_api_key: str

    # Groq
    groq_api_key: str = ""

    # OpenAI (keep for backward compat, optional)
    openai_api_key: str = ""

    # Azure Storage
    azure_storage_connection_string: str
    azure_storage_container_name: str = "documents"

    # Azure AI Search
    azure_search_endpoint: str
    azure_search_key: str
    azure_search_index_name: str = "rag-documents"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # ✅ ignore any extra keys in .env

@lru_cache()
def get_settings() -> Settings:
    return Settings()