################################
#   Create embeddings & index
################################

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pickle

# Load data
df = pd.read_csv("data.csv")

# Clean + add data
df["description"] = df["description"].fillna("")
df["categories"] = df["categories"].fillna("")

df["text"] = df["title"] + " " + df["description"] + " " + df["categories"]
df = df.dropna(subset=["text"])
df["text"] = df["text"].astype(str)

df["url"] = "https://www.amazon.com/dp/" + df["id"].astype(str)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(df["text"].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save index + metadata
faiss.write_index(index, "index.faiss")
df.to_pickle("metadata.pkl")

print("✅ Index built and saved!")