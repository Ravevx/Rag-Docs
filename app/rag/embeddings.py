from typing import List
from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embedding(text: str) -> List[float]:
    model = get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    model = get_model()
    embeddings = model.encode(texts, normalize_embeddings=True)
    return [e.tolist() for e in embeddings]