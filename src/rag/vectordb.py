CHROMA_PATH = "data/vectorstore"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def get_embedding_model():
    # Imported lazily so the heavy torch / sentence-transformers stack is not
    # loaded when the module is merely imported (e.g. at app start-up).
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

def get_vectorstore():
    from langchain_community.vectorstores import Chroma
    embedding = get_embedding_model()
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding
    )
