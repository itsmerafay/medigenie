from operator import index
from re import split
import os
import pymupdf
from cachetools import LRUCache
from django.conf import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader

from langchain.vectorstores import FAISS
from docmind.services.gemini import gemini_llm_response

# maxsize - size of objects that need to be kept in cache
# cache from cache.tool - for global cache
# cache from functools - for func level cache



_vector_cache = LRUCache(maxsize=128)


def pdf_upload_path(instance, filename):
    return f"uploads/{instance.user_id}/{instance.id}/{filename}"


# def _embeddings(model_name: str):
#     return HuggingFaceEmbeddings(model_name=model_name)


def build_index_from_pdf(pdf_path: str, index_dir: str, embedding_model: str):
    from docmind.utilities import get_embedder

    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    # Combine all pages into one big string
    text = "\n".join([doc.page_content for doc in documents])

    splitter = RecursiveCharacterTextSplitter(chunk_size=1800, chunk_overlap=10)
    chunks = splitter.split_text(text)

    embeddings = get_embedder(embedding_model)
    vectors = embeddings.embed_documents(chunks)
    vector_store = FAISS.from_embeddings(list(zip(chunks,vectors)), embedding=embeddings)

    abs_dir = os.path.join(settings.MEDIA_ROOT, index_dir) 
    os.makedirs(abs_dir, exist_ok=True)

    vector_store.save_local(abs_dir)
    _vector_cache[(index_dir, embedding_model)] = vector_store

    return vector_store


def load_index_fast(index_dir: str, embedding_model: str):
    from docmind.utilities import get_embedder

    key = (index_dir, embedding_model)
    store = _vector_cache.get(key)
    if store:
        return store
    
    abs_dir = os.path.join(settings.MEDIA_ROOT, index_dir)
    embs = get_embedder(embedding_model)

    store = FAISS.load_local(abs_dir, embs, allow_dangerous_deserialization=True)
    _vector_cache[key] = store

    return store


# def load_index(index_dir: str, embedding_model: str):
#     abs_dir = os.path.join(settings.MEDIA_ROOT, index_dir)
#     embs = _embeddings(embedding_model)
#     return FAISS.load_local(abs_dir, embs, allow_dangerous_deserialization=True)


def ask_with_rag(index_dir: str, query:str, embedding_model: str):
    vector_storage = load_index_fast(index_dir, embedding_model)
    docs = vector_storage.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""
    
    You are a helpful medical assistant. Answer strictly using the context

    Context:
    {context}

    Question: {query}

    Answer clearly and concisely.
    """

    for chunk in gemini_llm_response(prompt):
        yield chunk
