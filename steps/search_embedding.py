import logging

from zenml import step
from typing import List, Dict, Union, Any
import faiss
import pickle
import numpy as np

from src.search_embedding import FaissSearchEmbedding, SearchEmbedding

@step
def search_embedding(query_embedding: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Search for the most similar chunks based on the query embedding.
    Args:
        query_embedding (List[Dict[str, Any]]): The query embedding to be searched.

    Returns:
        List[Dict[str, Any]]: The list of matching chunks.
    """
    search = FaissSearchEmbedding()
    return search.search_embedding(query_embedding=query_embedding)