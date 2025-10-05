from functools import lru_cache

import torch

from langchain_huggingface import HuggingFaceEmbeddings


FAST_EMBED = "sentence-transformers/all-MiniLM-L6-v2"


# encode method is resp for (text to numerical vectors)
# batch_size is number of text/sentences to encode/vectorize at once
# normalize_embeddings - makes cosine similarity correct and stable

@lru_cache(maxsize=8)
def get_embedder(model_name: str = FAST_EMBED):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedder = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
        encode_kwargs = {"batch_size": 256, "normalize_embeddings": True}
    )

    return embedder
