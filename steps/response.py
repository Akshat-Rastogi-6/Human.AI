import logging
from zenml import step

from src.data_response import Response, GeminiResponse

@step
def response(matching_chunks, query):
    try:
        logging.info("Preparing response...")
        agent1 = GeminiResponse()
        resp = agent1.get_response(matching_chunks=matching_chunks, query=query)
        logging.info(f"Response: {resp}")
        return resp
    except Exception as e:
        logging.error(f"Error during response generation: {e}") 
        raise e
