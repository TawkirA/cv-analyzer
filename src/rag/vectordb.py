from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_PATH = "data/vectorstore"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def get_vectorstore():
    embedding = get_embedding_model()
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding
    )