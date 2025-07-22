from utils.parser import parse_documents
from mcp.message import create_message

class IngestionAgent:
    def __init__(self):
        pass

    def run(self, uploaded_files):
        chunks = parse_documents(uploaded_files)
        return create_message(
            sender="IngestionAgent",
            receiver="RetrievalAgent",
            type_="INGESTION_COMPLETE",
            payload={"chunks": chunks}
        )
