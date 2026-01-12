import streamlit as st
import os
from dotenv import load_dotenv

from rag.loader import load_pdf
from rag.chunker import chunk_documents
from rag.vectorstore import create_vectorstore
from rag.qa_chain import create_qa_chain

load_dotenv()

st.set_page_config(page_title="PDF RAG Chatbot", layout="wide")

st.title("📄 Chat With Your PDF")
st.write("Upload a PDF and ask questions. Answers come **only** from the document.")

# Session state
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

    if uploaded_file:
        file_path = os.path.join("data/uploads", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("PDF uploaded successfully")

        with st.spinner("Processing document..."):
            documents = load_pdf(file_path)
            chunks = chunk_documents(documents)
            vectorstore = create_vectorstore(chunks)
            st.session_state.qa_chain = create_qa_chain(vectorstore)

        st.success("Document indexed. You can now ask questions!")

    if st.button("Clear Chat"):
        st.session_state.chat_history = []

# Chat input
question = st.chat_input("Ask a question about the PDF")

if question and st.session_state.qa_chain:
    with st.spinner("Thinking..."):
        result = st.session_state.qa_chain(question)

        answer = result["result"]
        sources = result["source_documents"]

        st.session_state.chat_history.append(("user", question))
        st.session_state.chat_history.append(("assistant", answer))

        with st.expander("Sources"):
            for doc in sources:
                st.write(
                    f"📄 Page {doc.metadata.get('page', 'N/A')}: "
                    f"{doc.page_content[:300]}..."
                )

# Display chat
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)