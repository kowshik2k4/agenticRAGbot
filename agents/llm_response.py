import os
import google.generativeai as genai
from mcp.message import create_message

class LLMResponseAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY is not set in environment.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def run(self, message):
        context = "\n".join(message["payload"].get("retrieved_context", []))
        query = message["payload"].get("query", "")
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

        try:
            response = self.model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = f"❌ Gemini failed to generate a response: {str(e)}"

        return create_message(
            sender="LLMResponseAgent",
            receiver="UI",
            type_="LLM_RESPONSE",
            payload={
                "answer": answer,
                "sources": message["payload"].get("retrieved_context", [])
            }
        )

