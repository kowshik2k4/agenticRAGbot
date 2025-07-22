from openai import ChatCompletion
from mcp.message import create_message
import os

class LLMResponseAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    def run(self, message):
        context = "\n".join(message["payload"]["retrieved_context"])
        query = message["payload"]["query"]
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            api_key=self.api_key
        )

        return create_message(
            sender="LLMResponseAgent",
            receiver="UI",
            type_="LLM_RESPONSE",
            payload={
                "answer": response["choices"][0]["message"]["content"],
                "sources": message["payload"]["retrieved_context"]
            }
        )

