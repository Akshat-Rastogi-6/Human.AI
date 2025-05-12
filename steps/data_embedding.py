import logging
from zenml import step

from typing import List, Dict
from src.data_embedding import GoogleEmbedding


@step
def embedding(chunks: List[Dict[str, str]]) ->  List[Dict[str, str]]:
    """
    Embeds the data chunks using the Google embedding strategy.

    Args:
        chunks (List[Dict[str, str]]): The data chunks to be embedded.
    """
    try:
        logging.info("Starting data embedding...")
        embedding_strategy = GoogleEmbedding()
        embedded_data = embedding_strategy.embed_data(chunks)
        logging.info("Data embedding complete.")
        embedding_strategy.save_embedding(embedded_data, chunks)
        logging.info("Embedded data saved.")
        return embedded_data
    except Exception as e:
        logging.error(f"Error during data embedding: {e}")
        raise e
    
@step
def embedding_query(query: str)-> List[Dict[str, str]]:
    """
    Embeds the query using the Google embedding strategy.

    Args:
        query (str): The query to be embedded.
    """
    try:
        logging.info("Starting query embedding...")
        embedding_strategy = GoogleEmbedding()
        embedded_query = embedding_strategy.embed_query(query)
        logging.info("Query embedding complete.")
        return embedded_query
    except Exception as e:
        logging.error(f"Error during query embedding: {e}")
        raise e