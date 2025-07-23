import streamlit as st
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response import LLMResponseAgent

st.title("📚 Agentic RAG Chatbot")

uploaded_files = st.file_uploader("Upload your documents", accept_multiple_files=True)
query = st.text_input("Ask a question")
st.markdown(
        """
        <style>
        .block-container { padding-bottom: 100px !important; }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0e1117;
            text-align: center;
            padding: 10px;
            font-size: 0.9em;
            color: #f9f9f9;
            border-top: 1px solid #e6e6e6;
            z-index: 100;
        }
        </style>
        <div class="footer">
            © 2025 TalentScout AI. All rights reserved | Built with ❤️ using Streamlit | Sai Kowsik Tukuntla
        </div>
        """,
        unsafe_allow_html=True
    )
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

