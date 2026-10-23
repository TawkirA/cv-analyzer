# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from src.rag.vectordb import (get_embedding_model, CHROMA_PATH)

CHROMA_PATH = "data/vectorstore"
KB_PATH = "data/knowledge_base"
EMBED_MODEL = "-transformers/all-MiniLM-L6-v2"

def load_documents():
    loader = DirectoryLoader(KB_PATH, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    return loader.load()

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_documents(documents)

def create_vectorstore(chunks):
    embeddings = get_embedding_model()
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    vectordb.persist()
    return vectordb

def ingest_knowledge_base():
    print("Loading knowledge base documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")
    print("Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"Generated {len(chunks)} chunks")
    print("Creating vector database...")
    create_vectorstore(chunks)
    print("Knowledge base ingestion completed")
    
if __name__ == "__main__":
    ingest_knowledge_base()