import logging
from zenml import step
from typing import List, Dict
import pickle

from src.data_analysis import splitByHeading, DataAnalyzer, extractEntities

def save_chunks_to_pkl(chunks: List[Dict[str, str]], filename: str) -> None:
    with open(filename, 'wb') as file:
        pickle.dump(chunks, file)
    print(f"Data saved to {filename}")

@step
def chunk_data(data: str, data_path:str):
    try:
        headSplit = splitByHeading()
        split_statergy = DataAnalyzer(data, headSplit)
        headProcessedData = split_statergy.split_data(data_path)

        entitySplit = extractEntities()
        split_statergy = DataAnalyzer(data, entitySplit)
        entityProcessedData = split_statergy.split_data(data_path)

        sections = headProcessedData
        structured_data = {}
        for heading, content in sections.items():
            entities = entityProcessedData
            structured_data[heading] = {
                "content": content,
                "entities": entities
            }

        save_chunks_to_pkl(structured_data, "processed_chunks.pkl")
        return structured_data
    except Exception as e:
        logging.error(f"Error chunking data: {e}")
        raise e
