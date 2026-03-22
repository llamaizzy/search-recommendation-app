####################################
#   Query & Recommendation Logic
####################################

import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load everything once
index = faiss.read_index("index.faiss")
df = pickle.load(open("metadata.pkl", "rb"))
model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query, topk=5):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, topk)

    results = df.iloc[indices[0]].copy()
    results["score"] = distances[0]
    return results

def recommend(item_id, topk=5):
    matches = df[df["id"] == item_id]
    if len(matches) == 0:
        return None
    
    item_idx = int(matches.index[0])

    item_vec = index.reconstruct(item_idx).reshape(1, -1)
    distances, indices = index.search(item_vec, topk + 1)
    recs = df.iloc[indices[0][1:]].copy() # skip first result (itself)
    recs["score"] = distances[0][1:]
    return recs

