# agent.py
import faiss
import numpy as np
import requests
import pickle

INDEX_PATH = "index.faiss"
META_PATH = "metadata.pkl"

# -------- LOAD INDEX & METADATA --------
index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "rb") as f:
    store = pickle.load(f)

texts = store["texts"]
metadata = store["metadata"]

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

# -------- RETRIEVE RELEVANT CONTEXT --------
def retrieve_context(query, top_k=3):
    query_embedding = get_embedding(query).reshape(1, -1)
    _, indices = index.search(query_embedding, top_k)

    results = []
    for i in indices[0]:
        results.append({
            "text": texts[i],
            "metadata": metadata[i]
        })
    return results

# -------- MAIN AI AGENT FUNCTION --------
def ask_agent(case_context, user_question):
    search_query = f"{case_context}. {user_question}"
    sources = retrieve_context(search_query)

    if not sources:
        return {
            "answer": "No applicable information found. Manual review required.",
            "citations": [],
            "confidence": "low"
        }

    combined_sources = ""
    citations = []

    for s in sources:
        combined_sources += f"\n{s['text']}\n"
        citations.append(s["metadata"])

    prompt = f"""
You are an AI compliance assistant.

STRICT RULES:
- Use ONLY the provided sources.
- Do NOT invent information.
- If unsure, say manual review required.
- Always include citations.

SOURCES:
{combined_sources}

CASE CONTEXT:
{case_context}

QUESTION:
{user_question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return {
        "answer": response.json()["response"].strip(),
        "citations": citations,
        "confidence": "high"
    }

# -------- CHAT LOOP --------
print("\nAI Knowledge Agent (type 'exit' to quit)\n")

case_context = input("Enter case context: ")

while True:
    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    result = ask_agent(case_context, question)

    print("\n--- RESPONSE (Dictionary Format) ---")
    print(result)
