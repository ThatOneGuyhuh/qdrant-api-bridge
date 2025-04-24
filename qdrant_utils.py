import requests
import os

QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
COLLECTION = "devour_traits"

def get_embedding(text):
    res = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"input": text, "model": "text-embedding-ada-002"}
    )
    return res.json()["data"][0]["embedding"]

def embed_and_store(data):
    vector = get_embedding(data["text"])
    payload = {
        "vectors": [vector],
        "payload": [{"text": data["text"]}],
        "ids": [data.get("id", "auto")],
    }
    res = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION}/points",
        headers={"api-key": QDRANT_API_KEY, "Content-Type": "application/json"},
        json=payload
    )
    return res.json()

def search_vector(query):
    vector = get_embedding(query)
    payload = {
        "vector": vector,
        "top": 3,
        "with_payload": True
    }
    res = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
        headers={"api-key": QDRANT_API_KEY, "Content-Type": "application/json"},
        json=payload
    )
    return res.json()
