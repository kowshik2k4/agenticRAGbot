from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import os

def parse_documents(uploaded_files):
    chunks = []
    for file in uploaded_files:
        filename = file.name.lower()
        if filename.endswith(".pdf"):
            reader = PdfReader(file)
            chunks.extend([p.extract_text() for p in reader.pages if p.extract_text()])
        elif filename.endswith(".docx"):
            doc = Document(file)
            chunks.extend([p.text for p in doc.paragraphs if p.text.strip()])
        elif filename.endswith(".csv"):
            df = pd.read_csv(file)
            chunks.extend([row.to_string() for _, row in df.iterrows()])
        elif filename.endswith(".txt"):
            chunks.extend(file.read().decode("utf-8").splitlines())
    return chunks
