import logging

from PyPDF2 import PdfReader
from zenml import step

class IngestAnalyzeData:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def read_data(self):
        """
        Just Reads the data and takes out all the content of the Pdf
        """
        reader = PdfReader(self.pdf_path)
        text = " ".join(page.extract_text() for page in reader.pages)
        return text
    
@step
def ingest_data(data_path: str) -> str:
    """
    Ingests the data from the given path and returns it as a string.

    Args:
        data_path (str): The path to the PDF file.

    Returns:
        str: The text content of the PDF file.
    """
    try:
        logging.info(f"Reading data from {data_path}")
        ingest_analyze_data = IngestAnalyzeData(data_path)
        text = ingest_analyze_data.read_data()
        logging.info("Data ingestion complete.")
        return text
    except Exception as e:
        logging.error(f"Error reading data from {data_path}: {e}")
        raise e