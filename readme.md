# Human.AI

This project implements a Retrieval Augmented Generation (RAG) pipeline to analyze PDF documents, specifically designed for documents with personal information in this implementation. It allows users to ask questions about the content of a PDF, and the system will retrieve relevant information and generate a coherent answer.

## Features

- **PDF Ingestion:** Reads text content from PDF files.
- **Data Chunking:** Splits the extracted text into meaningful chunks based on headings and entities.
- **Embedding Generation:** Creates vector embeddings for text chunks and user queries using Google's Generative AI.
- **Vector Search:** Utilizes FAISS for efficient similarity search between query embeddings and document chunk embeddings.
- **Response Generation:** Leverages Google's Gemini model to generate answers based on retrieved chunks and the user's query.
- **ZenML Integration:** Orchestrates the entire process as a series of reproducible MLOps pipelines.

## Technologies Used

- **Python:** Core programming language.
- **ZenML:** MLOps framework for pipeline orchestration.
- **Google Generative AI:** For text embeddings (models/embedding-001) and response generation (gemini-1.5-flash).
- **FAISS:** For efficient similarity search in vector space.
- **Langchain:** Utilized for its Google Generative AI embedding components.
- **PyPDF2:** For reading text from PDF files.
- **spaCy:** For Named Entity Recognition (NER) during data chunking.
- **NumPy, Torch:** For numerical operations, especially with embeddings.
- **Flask (implied by waitress):** For potential future API deployment.
- **python-dotenv:** For managing environment variables.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Human.AI
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add your Google API Key:
    ```env
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    ```

5.  **Initialize ZenML (if not already done for your environment):**
    Follow the ZenML documentation for initializing ZenML and setting up a stack. The project uses a local default stack.

## Usage

1.  **Place your PDF:**
    Put the PDF file you want to analyze into the `data/` directory (e.g., `data/resume.pdf`). The `run_pipeline.py` script is currently hardcoded to use `data/resume.pdf`.

2.  **Run the pipelines:**
    Execute the `run_pipeline.py` script to run both the training (data processing and embedding) and testing (querying) pipelines:
    ```bash
    python run_pipeline.py
    ```
    This script will:
    *   First, run `train_pipeline` which ingests the PDF, chunks the data, creates embeddings, and saves them.
    *   Then, run `test_pipeline` with a predefined query ("What are your projects?") to demonstrate the RAG functionality. The response will be printed to the console.

3.  **Customize the query:**
    To ask different questions, modify the `query` variable in `run_pipeline.py` before execution:
    ```python
    # in run_pipeline.py
    query = "Your custom question here?"
    pipeline_run = test_pipeline(query=query)
    ```

## Project Structure

```
Human.AI/
├── .env                    # Environment variables (Google API Key)
├── .gitignore              # Files and directories to ignore
├── .zen/                   # ZenML metadata and configuration
├── data/
│   ├── chunks/
│   │   └── processed_chunks.pkl # Serialized processed text chunks
│   ├── vectors/
│   │   ├── document_metadata.pkl # Metadata for document chunks
│   │   └── resume_index.faiss    # FAISS index for embeddings
│   └── resume.pdf              # Example PDF (user needs to add this)
├── pipelines/
│   ├── __init__.py
│   ├── testing_pipline.py    # ZenML pipeline for querying
│   └── training_pipline.py   # ZenML pipeline for data processing and embedding
├── src/
│   ├── __init__.py
│   ├── data_analysis.py      # PDF parsing and chunking strategies
│   ├── data_embedding.py     # Embedding generation and saving logic
│   ├── data_response.py      # Response generation logic (using Gemini)
│   └── search_embedding.py   # FAISS embedding search logic
├── steps/
│   ├── __init__.py
│   ├── chunk_data.py         # ZenML step for chunking data
│   ├── data_embedding.py     # ZenML step for embedding data and queries
│   ├── ingest_analyze_data.py # ZenML step for ingesting PDF data
│   ├── response.py           # ZenML step for generating responses
│   └── search_embedding.py   # ZenML step for searching embeddings
├── __init__.py
├── readme.md                 # This file
├── requirements.txt          # Python dependencies
└── run_pipeline.py           # Script to execute ZenML pipelines
```

## How it Works

1.  **Training Pipeline (`training_pipeline.py`):**
    *   **Ingest Data (`ingest_data` step):** Reads the text from the specified PDF.
    *   **Chunk Data (`chunk_data` step):**
        *   Splits the text into sections based on identified headings.
        *   Extracts named entities from the text.
        *   Combines this information to create structured chunks (heading, content).
        *   Saves these chunks to `data/chunks/processed_chunks.pkl`.
    *   **Embed Data (`embedding` step):**
        *   Generates embeddings for each chunk's content using Google's `models/embedding-001`.
        *   Saves these embeddings into a FAISS index at `data/vectors/resume_index.faiss`.
        *   Saves metadata about the chunks to `data/vectors/document_metadata.pkl`.

2.  **Testing Pipeline (`testing_pipeline.py`):**
    *   **Embed Query (`embedding_query` step):** Takes a user query (string) and generates an embedding for it using the same Google model.
    *   **Search Embedding (`search_embedding` step):**
        *   Uses the FAISS index created by the training pipeline.
        *   Searches for the top N most similar document chunks to the query embedding.
    *   **Response (`response` step):**
        *   Takes the retrieved chunks and the original query.
        *   Constructs a prompt for the Gemini model, providing the chunks as context.
        *   Generates a natural language answer using the Gemini model.
        *   Prints the answer to the console.

## Future Improvements

*   **API Deployment:** Wrap the testing pipeline in a Flask (or other) API for easier interaction.
*   **More Sophisticated Chunking:** Explore advanced text splitting techniques for better context preservation.
*   **Metadata Filtering:** Allow filtering of chunks based on metadata before or during the search.
*   **Evaluation Metrics:** Implement metrics to evaluate the quality of retrieved chunks and generated responses.
*   **Support for More Document Types:** Extend beyond PDF to `.txt`, `.docx`, etc.
*   **User Interface:** Develop a simple web interface for uploading PDFs and asking questions.
*   **Error Handling and Logging:** Enhance robustness with more comprehensive error handling and detailed logging.
