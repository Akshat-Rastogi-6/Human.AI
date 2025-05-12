from pipelines.training_pipline import train_pipline
from zenml.client import Client

if __name__ == "__main__":
    # Initialize the ZenML client
    client = Client()

    # Define the path to your PDF file
    pdf_path = "data\Akshat_Rastogi_Resume_SDE (1).pdf"

    # Run the pipeline with the specified PDF path
    pipeline_run = train_pipline(data_path=pdf_path)
    print(f"Pipeline run started with ID: {pipeline_run.id}")