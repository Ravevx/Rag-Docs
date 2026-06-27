import os
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from app.rag.embeddings import generate_embedding
import uuid

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = "rag-documents"


def get_index_client():
    return SearchIndexClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )


def get_search_client():
    return SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY)
    )


def create_index():
    client = get_index_client()

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="filename", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=384,
            vector_search_profile_name="hnsw-profile"
        ),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
        profiles=[VectorSearchProfile(name="hnsw-profile", algorithm_configuration_name="hnsw")]
    )

    index = SearchIndex(name=INDEX_NAME, fields=fields, vector_search=vector_search)

    # Only create if index doesn't exist — never delete existing data
    existing = [i for i in client.list_index_names()]
    if INDEX_NAME not in existing:
        client.create_index(index)
        print(f"Index '{INDEX_NAME}' created successfully")
    else:
        print(f"Index '{INDEX_NAME}' already exists — skipping creation")


def index_chunks(chunks: list[str], filename: str):
    search_client = get_search_client()

    documents = []
    for chunk in chunks:
        embedding = generate_embedding(chunk)
        documents.append({
            "id": str(uuid.uuid4()),
            "content": chunk,
            "filename": filename,
            "embedding": embedding
        })

    search_client.upload_documents(documents)
    print(f"Indexed {len(documents)} chunks from '{filename}'")