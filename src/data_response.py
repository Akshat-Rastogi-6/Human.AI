import logging

from abc import ABC, abstractmethod
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv('.env')


class Response(ABC):
    """
    Abstract class for response strategies.
    """

    @abstractmethod
    def get_response(self, matching_chunks, query) -> str:
        """
        Abstract method to get the response.
        """
        pass

class GeminiResponse(Response):
    """
    Gemini response strategy.
    """

    def get_response(self, matching_chunks, query) -> str:
        """
        Get the response from the Gemini model.
        """
        # Extract content from dictionaries
        text_chunks = []
        for chunk in matching_chunks:
            # Extract the content field from each dictionary
            if isinstance(chunk, dict) and "content" in chunk:
                text_chunks.append(chunk["content"])
            elif isinstance(chunk, str):
                text_chunks.append(chunk)
        
        # Join the text chunks
        context = "\n".join(text_chunks)
        input_prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer:"

        # Generate response
        llm = genai.GenerativeModel('gemini-1.5-flash')
        response = llm.generate_content(input_prompt)

        print(response.text)
        return response.text