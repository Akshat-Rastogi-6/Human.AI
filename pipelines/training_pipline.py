from zenml import pipeline

from steps.ingest_analyze_data import ingest_data
from steps.chunk_data import chunk_data
from steps.data_embedding import embedding


@pipeline
def train_pipline(data_path: str):
    """
    Pipeline to train the model.
    Args:
        data_path (str): The path to the PDF file.
    """
    data = ingest_data(data_path=data_path)  #will get text from the pdf
    data_chunk = chunk_data(data=data, data_path=data_path)  #will chunk the data and save it in a .pkl file and store it in data/chunks
    data_embedding = embedding(chunks=data_chunk)  #will embed the data and save the embedding in a .faiss file and store it in data/vectors
    