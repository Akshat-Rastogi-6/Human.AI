"""
Human.AI - A Retrieval Augmented Generation (RAG) pipeline for document analysis

This package provides functionality to process PDF documents, create embeddings,
and answer questions about document content using Google's Generative AI.
"""

__version__ = "0.1.0"

import logging

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Expose key components for easy imports
from pipelines.training_pipline import train_pipline  # noqa
from pipelines.testing_pipline import test_pipeline  # noqa

# Define what's available when using `from human_ai import *`
__all__ = [
    "train_pipline",
    "test_pipeline",
]