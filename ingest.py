# ingest.py

'''ollama_rag_agent/
│
├── ingest.py          ← run this file
├── agent.py           ← run later for chatting
├── data/              ← REQUIRED
│   ├── policy_1.pdf
│   ├── sop_manual.pdf
│   ├── regulation_doc.pdf
│
├── index.faiss        ← auto-created
├── metadata.pkl       ← auto-created
'''
import fitz  # PyMuPDF
import faiss
import numpy as np
import requests
import pickle
import os

DATA_DIR = "data"
INDEX_PATH = "index.faiss"
META_PATH = "metadata.pkl"

# -------- OLLAMA EMBEDDING FUNCTION --------
def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "llama3.2",
            "prompt": text
        }
    )
    return np.array(response.json()["embedding"], dtype="float32")

texts = []
metadata = []

# -------- INGEST MULTIPLE DOCUMENTS --------
for file_name in os.listdir(DATA_DIR):
    if not file_name.endswith(".pdf"):
        continue

    file_path = os.path.join(DATA_DIR, file_name)
    doc = fitz.open(file_path)

    # Identify source type by filename (simple demo logic)
    if "policy" in file_name.lower():
        doc_type = "policy"
    elif "sop" in file_name.lower():
        doc_type = "sop"
    else:
        doc_type = "regulation"

    for page_number, page in enumerate(doc):
        text = page.get_text().strip()
        if not text:
            continue

        texts.append(text)
        metadata.append({
            "source": file_name,
            "type": doc_type,
            "page": page_number + 1
        })

# -------- CREATE VECTOR INDEX --------
embeddings = [get_embedding(t) for t in texts]
dimension = len(embeddings[0])

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, INDEX_PATH)

with open(META_PATH, "wb") as f:
    pickle.dump({"texts": texts, "metadata": metadata}, f)

print("Ingestion complete. Documents indexed successfully.")
