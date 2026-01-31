import argparse
import logging
from crawler import WebCrawler
from processor import TextProcessor
from storage import VectorStore
from rag import RAGPipeline
import uvicorn
from app import app
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_pipeline(url, max_pages=5):
    """
    Crawl, process, and index a website.
    """
    logger.info(f"Starting initialization for: {url}")
    
    # 1. Crawl
    crawler = WebCrawler(url, max_pages=max_pages)
    crawler.crawl()
    pages = crawler.get_all_content()
    
    if not pages:
        logger.error("No content crawled. Exiting.")
        return None

    # 2. Process/Chunk
    processor = TextProcessor(chunk_size=1000, overlap=200)
    chunks = processor.process_pages(pages)
    
    # 3. Embed and Store
    vector_store = VectorStore()
    vector_store.create_index(chunks)
    
    return vector_store

def main():
    parser = argparse.ArgumentParser(description="RAG Q&A Bot CLI")
    parser.add_argument("--url", type=str, help="Website URL to index")
    parser.add_argument("--max-pages", type=int, default=5, help="Max pages to crawl")
    parser.add_argument("--serve", action="store_true", help="Start the API server")
    
    args = parser.parse_args()

    if args.url:
        vector_store = initialize_pipeline(args.url, args.max_pages)
        if vector_store and not args.serve:
            # Demonstration if not serving
            pipeline = RAGPipeline(vector_store)
            query = "What is this website about?"
            print(f"\nExample Query: {query}")
            result = pipeline.ask(query)
            print(f"Answer: {result['answer']}")
    
    if args.serve:
        logger.info("Starting API server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
