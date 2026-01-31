RAG Q&A Support Bot

A Python-based Retrieval Augmented Generation support bot that crawls websites and answers questions based on the extracted content.

Features
1. Website Crawler: Extracts text from target URLs and subpages.
2. Text Processor: Chunks content with overlapping windows for context.
3. Local Storage: Uses FAISS and local embeddings for similarity search.
4. Q&A Pipeline: Generates answers using OpenAI with retrieval context.
5. FastAPI: Provides a web endpoint for querying the bot.

Installation
1. Install Python 3.8 or higher.
2. Install dependencies by running: pip install -r requirements.txt
3. Create a .env file in the root directory.
4. Add your OpenAI API key to the .env file: OPENAI_API_KEY=your_key_here

Usage
1. To index a website, run: python main.py --url URL --max-pages 5
2. To start the API server, run: python main.py --serve
3. To ask a question, send a POST request to http://localhost:8000/ask with JSON body: {"question": "your question"}
4. Visit http://localhost:8000/docs for the interactive API documentation.

Project Files
1. crawler.py: Scraping and data extraction.
2. processor.py: Text cleaning and chunking.
3. storage.py: Vector database and search logic.
4. rag.py: Retrieval and answer generation.
5. app.py: FastAPI server code.
6. main.py: CLI tool to run the system.

License
Licensed under the MIT License.
