from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

def create_vectorstore(chunks):
    embeddings = OllamaEmbeddings(model="llama3")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore