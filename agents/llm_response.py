import os
import google.generativeai as genai
from mcp.message import create_message

class LLMResponseAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def run(self, message):
        context = "\n".join(message["payload"]["retrieved_context"])
        query = message["payload"]["query"]
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

        response = self.model.generate_content(prompt)

        return create_message(
            sender="LLMResponseAgent",
            receiver="UI",
            type_="LLM_RESPONSE",
            payload={
                "answer": response.text,
                "sources": message["payload"]["retrieved_context"]
            }
        )
