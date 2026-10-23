from src.rag.vectordb import get_vectorstore

vectordb = get_vectorstore()

def retrieve_context(query: str, k: int = 5) -> str:
    documents = vectordb.similarity_search(query=query, k=k)
    contexts = []
    for doc in documents:
        contexts.append(doc.page_content)
    return "\n\n".join(contexts)
    
        
    