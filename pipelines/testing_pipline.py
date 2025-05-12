from zenml import pipeline

from steps.data_embedding import embedding_query
from steps.search_embedding import search_embedding
from steps.response import response

@pipeline(enable_cache=False)
def test_pipeline(query: str):
    """
    Test pipeline to validate the functionality of the training pipeline.
    Args:
        query (str): The query to the file.
    """
    query_embedding = embedding_query(query=query)  #will embed the data and save the embedding in a .faiss file and store it in data/vectors
    query_embedding_search = search_embedding(query_embedding=query_embedding)  #will search the embedding and return the result
    res = response(matching_chunks=query_embedding_search, query=query)  #will prepare the generative ai response
    print(res)  #will print the response
