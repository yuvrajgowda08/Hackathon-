# Hackathon-
Project Title
Research Paper RAG Assistant

Problem Statement
Researchers and students often need to read multiple research papers to understand a topic, compare methods, or extract key information. This process is time-consuming and inefficient because users must manually search through long PDFs to find relevant sections such as methodology, datasets, and conclusions. Traditional search tools cannot understand context or answer questions directly from research papers.

Proposed Solution
We propose a Retrieval Augmented Generation (RAG) based assistant that allows users to upload research papers in PDF format and ask questions about them.
The system extracts the content from the documents, converts it into embeddings, stores them in a vector database, and retrieves the most relevant sections when a user asks a query. An LLM then generates a contextual answer based on the retrieved information.
This allows users to quickly summarize papers, compare methods, and extract insights without manually reading entire documents.

Features
Upload and process multiple research papers in PDF format
Ask natural language questions about the uploaded papers
Context-aware answers generated using RAG architecture
Automatic summarization and information extraction from documents
Fast semantic search across multiple research papers
Tech Stack
Language: Python
Framework: Streamlit
Database: FAISS (Vector Database)
Tools: LangChain, Sentence Transformers, Ollama / LLM, PyPDF

How It Works
The user uploads one or more research papers in PDF format.
The system extracts text from the PDFs.
The extracted text is split into smaller chunks.
Each chunk is converted into embeddings using a sentence transformer model.
The embeddings are stored in a FAISS vector database.
When the user asks a question, the system converts the query into an embedding.
FAISS retrieves the most relevant document chunks.
These retrieved chunks are sent to the LLM.
The LLM generates a context-aware answer based on the retrieved information.

Future Scope
Support for more document formats such as DOCX and web articles
Multi-document comparison and automated literature review generation
Citation extraction and reference highlighting
Integration with academic databases like IEEE or arXiv
Voice-based interaction with the research assistant

Team Members
A Yuv Raj
Charanya S
Dhanush Gowda N A
Lakshmi


## Improvements
- Improved performance by caching document processing
- Optimized retrieval using top-k search

## Bug Fix
- Fixed duplicate similarity output in paper comparison
- Used session_state to prevent repeated display
