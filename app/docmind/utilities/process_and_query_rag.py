from operator import index
from re import split
import os
import pymupdf
from cachetools import LRUCache
from django.conf import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader

from langchain_community.vectorstores import FAISS
from docmind.services.gemini import gemini_llm_response

# maxsize - size of objects that need to be kept in cache
# cache from cache.tool - for global cache
# cache from functools - for func level cache



_vector_cache = LRUCache(maxsize=32)


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

# import requests
# from django.conf import settings

# FASTAPI_URL = "https://itsmerafay-medigenie.hf.space/build-index/"

# def build_index_from_pdf_remote(pdf_path: str, embedding_model: str):
#     with open(pdf_path, "rb") as f:
#         files = {"file": f}
#         data = {"embedding_model": embedding_model}
#         response = requests.post(FASTAPI_URL, files=files, data=data)
        
#     if response.status_code != 200:
#         raise Exception(f"Index build failed: {response.text}")

#     # Save the returned zip file locally
#     zip_path = os.path.join(settings.MEDIA_ROOT, "index.zip")
#     with open(zip_path, "wb") as f:
#         f.write(response.content)

#     return zip_path




import os
import requests
from django.conf import settings

FASTAPI_URL = "https://itsmerafay-medigenie.hf.space/build-index/"

def build_index_from_pdf_remote(pdf_path: str, embedding_model: str, save_dir: str) -> str:
    """
    Sends PDF to remote FastAPI service, downloads index.zip, and saves it in `save_dir`.
    Returns the full path of the saved zip file.
    """
    os.makedirs(save_dir, exist_ok=True)

    with open(pdf_path, "rb") as f:
        files = {"file": f}
        data = {"embedding_model": embedding_model}
        response = requests.post(FASTAPI_URL, files=files, data=data)

    if response.status_code != 200:
        raise Exception(f"❌ Index build failed: {response.text}")

    zip_path = os.path.join(save_dir, "index.zip")
    with open(zip_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved remote index to: {zip_path}")
    return zip_path



# def load_index_fast(index_dir: str, embedding_model: str):
#     from docmind.utilities import get_embedder

#     key = (index_dir, embedding_model)
#     store = _vector_cache.get(key)
#     if store:
#         return store
    
#     abs_dir = os.path.join(settings.MEDIA_ROOT, index_dir)
#     embs = get_embedder(embedding_model)

#     store = FAISS.load_local(abs_dir, embs, allow_dangerous_deserialization=True)
#     _vector_cache[key] = store

#     return store

# import os
# import zipfile
# from django.conf import settings

# def unzip_index_if_needed(abs_dir):
#     zip_path = os.path.join(abs_dir, "index.zip")
#     if os.path.exists(zip_path):
#         print(f"📦 Found zip at: {zip_path} — extracting...")
#         with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#             zip_ref.extractall(abs_dir)
#         print("✅ Extraction done.")
#     else:
#         print("❌ No zip found at:", zip_path)

# def load_index_fast(index_dir, embedding_model):
#     from langchain_community.vectorstores import FAISS
#     from docmind.utilities import get_embedder

#     abs_dir = os.path.join(settings.MEDIA_ROOT, index_dir)
#     print("🔍 Looking for index in:", abs_dir)

#     unzip_index_if_needed(abs_dir)

#     # 🧪 List files inside the folder to confirm
#     print("📂 Contents of index dir:", os.listdir(abs_dir))

#     embs = get_embedder(embedding_model)

#     store = FAISS.load_local(abs_dir, embs, allow_dangerous_deserialization=True)
#     return store



import zipfile

# --- Global cache for FAISS stores ---
_loaded_indexes = {}

def unzip_index_if_needed(abs_dir):
    zip_path = os.path.join(abs_dir, "index.zip")
    if os.path.exists(zip_path):
        # ✅ Sirf tab unzip karo jab .faiss file nahi mili ho
        if not any(fname.endswith(".faiss") for fname in os.listdir(abs_dir)):
            print(f"📦 Found zip at: {zip_path} — extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(abs_dir)
            print("✅ Extraction done.")
    else:
        print("❌ No zip found at:", zip_path)


def load_index_fast(index_dir, embedding_model):
    from langchain_community.vectorstores import FAISS
    from docmind.utilities import get_embedder

    key = (index_dir, embedding_model)
    if key in _loaded_indexes:
        print("✅ Reusing cached FAISS index from memory")
        return _loaded_indexes[key]

    abs_dir = os.path.join(settings.MEDIA_ROOT, index_dir)
    print("🔍 Looking for index in:", abs_dir)

    unzip_index_if_needed(abs_dir)

    print("📂 Contents of index dir:", os.listdir(abs_dir))

    embs = get_embedder(embedding_model)
    store = FAISS.load_local(abs_dir, embs, allow_dangerous_deserialization=True)

    # ✅ Cache the store in RAM for reuse
    _loaded_indexes[key] = store
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

    Answer clearly and from the doctors perspective and with in the given context of the document.
    """

    for chunk in gemini_llm_response(prompt):
        yield chunk
