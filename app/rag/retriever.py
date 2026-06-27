import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
from app.rag.embeddings import generate_embedding
from dotenv import load_dotenv

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = "rag-documents"


def search_documents(query: str, top_k: int = 5) -> list[str]:
    client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )

    query_embedding = generate_embedding(query)

    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields="embedding"
    )

    results = client.search(
        search_text=query,
        vector_queries=[vector_query],
        select=["content", "filename"],
        top=top_k
    )

    return [doc["content"] for doc in results]