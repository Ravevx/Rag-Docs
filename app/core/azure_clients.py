from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
from app.core.config import get_settings

settings = get_settings()


def get_blob_client() -> BlobServiceClient:
    return BlobServiceClient.from_connection_string(
        settings.azure_storage_connection_string
    )


def get_search_client() -> SearchClient:
    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index_name,
        credential=AzureKeyCredential(settings.azure_search_key)
    )


def get_search_index_client() -> SearchIndexClient:
    return SearchIndexClient(
        endpoint=settings.azure_search_endpoint,
        credential=AzureKeyCredential(settings.azure_search_key)
    )


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)