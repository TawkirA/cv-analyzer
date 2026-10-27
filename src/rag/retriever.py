import threading

from src.rag.vectordb import get_vectorstore

_vectordb = None
_vectordb_lock = threading.Lock()


def get_vectordb():
    """
    Lazily loads the vector store (and its embedding model) once.
    Loading torch / sentence-transformers is slow, so it is deferred from import
    time and can be pre-warmed in a background thread via warm_up_vectordb().
    """
    global _vectordb
    if _vectordb is None:
        with _vectordb_lock:
            if _vectordb is None:
                _vectordb = get_vectorstore()
    return _vectordb


def warm_up_vectordb() -> None:
    """Pre-loads the vector store; safe to call from a background thread."""
    try:
        get_vectordb()
    except Exception:
        # Errors resurface (with full context) on the first real retrieval.
        pass


def retrieve_context(query: str, k: int = 5) -> str:
    documents = get_vectordb().similarity_search(query=query, k=k)
    contexts = []
    for doc in documents:
        contexts.append(doc.page_content)
    return "\n\n".join(contexts)
