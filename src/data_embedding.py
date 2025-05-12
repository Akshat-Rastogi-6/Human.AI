import logging
from abc import ABC, abstractmethod

from typing import List, Dict
import torch
import numpy as np
import faiss
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv('.env')

class DataEmbedding(ABC):
    """
    Abstract class for data embedding strategies.
    """

    @abstractmethod
    def embed_data(self, chunks: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Abstract method to embed the data.
        """
        pass

class GoogleEmbedding(DataEmbedding):
    """
    Google embedding strategy.
    """

    def embed_data(self, chunks: List[Dict[str, str]]) -> List[Dict[str, str]]:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        result = []
        for chunk in chunks:
            # Extract heading and content
            heading = chunk.get("heading", "")
            content = chunk.get("content", "")

            if isinstance(content, str) and content.strip():
                # Concatenate heading and content for embedding
                combined_text = f"{heading}: {content}".strip()
                try:
                    embedding = embeddings.embed_query(combined_text)
                    # Store embedding in the chunk
                    chunk["embedding"] = embedding
                    result.append(chunk)
                except Exception as e:
                    logging.error(f"Error embedding chunk '{heading}': {e}")
                    raise e

        return result
    
    def save_embedding(self, embeddings: List[Dict[str, str]], chunks: List[Dict[str, str]]) -> None:
        """
        Save the embeddings to a file using direct FAISS implementation.
        
        Args:
            embeddings (List[Dict[str, str]]): The embeddings to be saved
            chunks (List[Dict[str, str]]): The original text chunks
        """
        try:
            embedding_vectors = []
            for chunk in embeddings:
                if "embedding" in chunk:
                    embedding_vectors.append(chunk["embedding"])
            
            tensor = torch.tensor(embedding_vectors, dtype=torch.float32)
            
            np_embeddings = np.array([embedding.cpu().numpy() for embedding in tensor])
            
            os.makedirs(r"data\vectors", exist_ok=True)
            
            vector_dim = np_embeddings.shape[1] 
            index = faiss.IndexFlatL2(vector_dim) 
            
            # Add embeddings to the index
            index.add(np_embeddings)
            
            # Save the FAISS index
            faiss.write_index(index, r"data\vectors\resume_index.faiss")
            
            logging.info(f"Saved {len(embedding_vectors)} embeddings to FAISS index")
            
            self._save_metadata(chunks, r"data\vectors\document_metadata.pkl")
            
        except Exception as e:
            logging.error(f"Error saving embeddings: {e}")
            raise e
        
    def _save_metadata(self, chunks: List[Dict[str, str]], filepath: str) -> None:
        """Save document metadata for later retrieval"""
        import pickle
        
        metadata = []
        for chunk in chunks:
            metadata.append({
                "heading": chunk.get("heading", ""),
                "content": chunk.get("content", "")
            })
        
        with open(filepath, 'wb') as f:
            pickle.dump(metadata, f)