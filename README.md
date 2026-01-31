# RAG Q&A Support Bot

A modular Python-based Retrieval Augmented Generation (RAG) system that crawls websites, indexes content using FAISS and local embeddings, and provides a Q-A API.

## Features

- **Web Crawler**: Automatically extracts text content from a target website.
- **Smart Chunking**: Splits text into overlapping segments for better context retention.
- **Local Embeddings**: Uses `sentence-transformers` for efficient, local vector generation.
- **Vector Store**: FAISS-based high-performance similarity search.
- **RAG Pipeline**: Context-aware answer generation using OpenAI (with local mock fallbacks).
- **FastAPI Endpoint**: Clean REST API for querying the bot.

## Installation

1. **Clone and Install**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file and add your OpenAI API key (optional for local mock mode):
   ```env
   OPENAI_API_KEY=your_key_here
   ```

## Usage

### 1. Initialize and Index a Website
Crawl and index a website to build the knowledge base:
```bash
python main.py --url https://docs.python.org/3/tutorial/index.html --max-pages 5
```

### 2. Run the API Server
```bash
python main.py --serve
```

### 3. Ask Questions
Query the bot via the `/ask` endpoint:
```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"What is Python?\"}"
```
Or use the interactive UI at `http://localhost:8000/docs`.

## Project Structure

- `crawler.py`: Website scraping and HTML cleaning.
- `processor.py`: Text cleaning and overlapping chunking logic.
- `storage.py`: Vector search engine using FAISS.
- `rag.py`: Orchestration of retrieval and generation.
- `app.py`: FastAPI application.
- `main.py`: CLI entry point.

## License
MIT
