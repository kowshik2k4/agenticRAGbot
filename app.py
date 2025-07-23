import streamlit as st
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response import LLMResponseAgent

st.title("📚 Agentic RAG Chatbot")

uploaded_files = st.file_uploader("Upload your documents", accept_multiple_files=True)
query = st.text_input("Ask a question")

if uploaded_files and query:
    ingestion = IngestionAgent()
    retrieval = RetrievalAgent()
    llm = LLMResponseAgent()

    msg1 = ingestion.run(uploaded_files)
    msg2 = retrieval.run(msg1)
    msg3 = retrieval.run({"type": "QUERY", "payload": {"query": query}})
    msg4 = llm.run(msg3)

    st.markdown("### Answer")
    st.write(msg4["payload"]["answer"])

    with st.expander("🔍 Sources"):
        for src in msg4["payload"]["sources"]:
            st.write("-", src)

