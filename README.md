# Legal RAG ChatBot – Technology Law Assistant

## Overview
This project is a Retrieval-Augmented Generation (RAG) chatbot built for learning purposes.
The chatbot answers questions related to technology law by retrieving relevant information from legal PDF documents and generating responses using a Large Language Model (LLM).

This project is intended for study and experimentation only and does not provide legal advice.

## Legal Domains Covered
The knowledge base consists of legal PDF documents related to:
- Cybersecurity and information security
- Data security and data protection
- Personal data protection and privacy management
- Electronic transactions and digital signatures
- Regulations on document confidentiality and information security

## RAG Workflow
The system follows a standard RAG pipeline:
PDF documents are loaded and split into smaller text chunks.
Each chunk is converted into embeddings using an embedding model.
The embeddings are stored in a FAISS vector database.
When a user asks a question, the retriever finds the most relevant chunks.
The LLM uses the retrieved context to generate an answer.


## Technologies Used
- Python
- LangChain
- FAISS (vector database)
- Embedding models
- Large Language Models (LLM)
- Jupyter Notebook


## Notes on Jupyter Notebooks (Google Colab)
All Jupyter Notebook files (`.ipynb`) in this project were **developed and executed using Google Colab**.

- The notebooks may include Colab-specific settings such as:
  - Google Drive mounting
  - File paths adapted for Colab environments
- To run these notebooks locally, minor adjustments to paths or environment setup may be required.

Using Google Colab allows:
- Faster experimentation
- Access to free GPU/TPU resources
- Easy sharing for learning and demonstration purposes

## How to Run
Install dependencies using:
pip install -r requirements.txt

If you want to rebuild the vector database from the PDF files, run:
create_vectorstore.ipynb

To start the chatbot application:
python app.py


## Notes on Data and Vectorstore
This repository includes a small set of PDF files and a prebuilt vectorstore so that the chatbot can run immediately for learning and demonstration.
In real-world or production systems, raw data and vector databases should not be committed to GitHub and should be rebuilt or stored externally.

## Learning Objectives
This project helps practice:
- Building an end-to-end RAG system
- Processing legal documents for question answering
- Chunking, embedding, and semantic retrieval
- Integrating LLMs with external knowledge sources

## Disclaimer
This chatbot is not a legal advisor.
All generated responses are for educational purposes only and should not be used for real legal decisions.

