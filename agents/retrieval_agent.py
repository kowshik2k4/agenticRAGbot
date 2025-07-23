import torch
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from mcp.message import create_message

class RetrievalAgent:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)  # ❌ DO NOT use .to() — REMOVE this line!
        self.index = faiss.IndexFlatL2(384)
        self.chunks = []

    def store_chunks(self, chunks):
        embeddings = self.model.encode(chunks, device=self.device)
        self.index.add(np.array(embeddings))
        self.chunks.extend(chunks)

    def retrieve(self, query):
        q_embedding = self.model.encode([query], device=self.device)
        D, I = self.index.search(np.array(q_embedding), 5)
        results = [self.chunks[i] for i in I[0] if i < len(self.chunks)]
        return results

    def run(self, message):
        if message["type"] == "INGESTION_COMPLETE":
            self.store_chunks(message["payload"]["chunks"])
        elif message["type"] == "QUERY":
            top_chunks = self.retrieve(message["payload"]["query"])
            return create_message(
                sender="RetrievalAgent",
                receiver="LLMResponseAgent",
                type_="RETRIEVAL_RESULT",
                payload={"retrieved_context": top_chunks, "query": message["payload"]["query"]}
            )
