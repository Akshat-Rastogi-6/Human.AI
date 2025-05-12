import logging
from typing import Dict, List, Union, Tuple
from abc import ABC, abstractmethod

import pdfplumber
import spacy
import re

nlp = spacy.load("en_core_web_sm")

class DataStrategy(ABC):
    '''
    Abstract class for mainitaing the data strategy
    '''

    @abstractmethod
    def split_data(self, data:str, path: str) -> Union[List[str], List[Tuple[str, str]]]:
        '''
        Abstract method to split the data
        '''
        pass

class splitByHeading(DataStrategy):

    def extract_headings_from_pdf(self, pdf_path: str) -> List[str]:
        headings = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')
                for line in lines:
                    # Detect potential headings (e.g., single line, title case, or numbered)
                    if re.match(r"^[A-Z][a-zA-Z ]{3,}$", line) or re.match(r"^\d+\.\s[A-Z].+$", line):
                        headings.append(line.strip())
        return list(set(headings))  # Remove duplicates
    
    def split_data(self, data: str, path: str) -> Dict[str, str]:
        """
        Splits the data into sections based on headings.
        Args:
            data (str): The text content of the PDF file.
            path (str): The path to the PDF file.

        Returns:
            Dict[str, str]: A dictionary where keys are headings and values are the corresponding sections.    
        """
        headings = self.extract_headings_from_pdf(path)
        sections = {}
        for heading in headings:
            pattern = rf"{re.escape(heading)}\n(.+?)(?=\n[A-Z][a-z]|$)"
            match = re.search(pattern, data, re.DOTALL)
            if match:
                sections[heading] = match.group(1).strip()
        return sections
    
class extractEntities(DataStrategy):
    def split_data(self, data:str, path: str=None) -> List[Tuple[str, str]]:
        """
        Splits the data into entities and context.
        Args:
            data (str): The text content of the PDF file.
        Returns:
            List[str]: A list of entities extracted from the text.
        """
        doc = nlp(data)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    
class DataAnalyzer:
    def __init__(self, data:str, strategy: DataStrategy):
        self.data = data
        self.strategy = strategy
    def split_data(self, path: str) -> Union[List[str], List[Tuple[str, str]]]:
        """
        Splits the data using the provided strategy.
        Args:
            path (str): The path to the PDF file.
        Returns:
            Union[List[str], List[Tuple[str, str]]]: The split data based on the strategy.
        """
        try:
            return self.strategy.split_data(self.data, path)
        except Exception as e:
            logging.error(f"Error splitting data: {e}")
            raise e
        

    
    


