import logging
from typing import List, Dict
import faiss
import numpy as np
import pickle
from abc import ABC, abstractmethod

class SearchEmbedding(ABC):
    """
    Abstract class for search embedding strategies.
    """

    @abstractmethod
    def search_embedding(self, query_embedding: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Abstract method to search the embedding.
        """
        pass

class FaissSearchEmbedding(SearchEmbedding):
    """
    FAISS search embedding strategy.
    """
    def search_embedding(self, query_embedding: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Search for the most similar chunks based on the query embedding.
        """
        try:
            # Extract the actual embedding vector
            if not query_embedding or "embedding" not in query_embedding[0]:
                raise ValueError("Query embedding missing or invalid format")
                
            query_vector = np.array(query_embedding[0]["embedding"], dtype='float32')
            query_embedding_array = np.expand_dims(query_vector, axis=0)
            
            # Load index and chunked data
            index = faiss.read_index(r"data\vectors\resume_index.faiss")
            with open(r"data\chunks\processed_chunks.pkl", 'rb') as f:
                chunked = pickle.load(f)
            
            # Perform search
            distances, indices = index.search(query_embedding_array, 3)
            
            # Get matching chunks
            matching_chunks = [chunked[i] for i in indices[0] if 0 <= i < len(chunked)]
            return matching_chunks
            
        except Exception as e:
            logging.error(f"Error searching embeddings: {e}")
            raise e