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
def chunk_data(data: str, data_path: str) -> List[Dict[str, str]]:
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

        result_list = []
        for key, value in structured_data.items():
            # Extract the string content from the dictionary
            content_text = value["content"]
            # Create a chunk with string content (not nested dictionary)
            chunk_dict = {
                "heading": key,
                "content": content_text  # Now it's a string
                # Optionally include entities as another top-level field if needed
                # "entities": value["entities"]
            }
            result_list.append(chunk_dict)

        save_chunks_to_pkl(result_list, "data\chunks\processed_chunks.pkl")
        return result_list
    except Exception as e:
        logging.error(f"Error chunking data: {e}")
        raise e
