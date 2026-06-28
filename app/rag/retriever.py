from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
from app.rag.embeddings import get_query_embedding
from app.core.config import get_settings

settings = get_settings()

def search_documents(query: str, top_k: int = 5) -> list[str]:
    client = SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index_name,
        credential=AzureKeyCredential(settings.azure_search_key)
    )

    query_embedding = get_query_embedding(query)  # ✅ uses retrieval_query task type

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