import torch
import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
from mcp.message import create_message

class RetrievalAgent:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load model/tokenizer manually to avoid SentenceTransformer internals
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

        self.index = faiss.IndexFlatL2(384)
        self.chunks = []

    def encode(self, texts):
        with torch.no_grad():
            encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(self.device)
            model_output = self.model(**encoded_input)
            embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
            return embeddings.cpu().numpy()

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element is token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / input_mask_expanded.sum(1)

    def store_chunks(self, chunks):
        embeddings = self.encode(chunks)
        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def retrieve(self, query):
        query_embedding = self.encode([query])
        D, I = self.index.search(query_embedding, 5)
        results = [self.chunks[i] for i in I[0] if i < len(self.chunks)]
        return results

    def run(
