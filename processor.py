import re
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """
    Handles text cleaning and chunking for RAG.
    """
    def __init__(self, chunk_size=500, overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def clean_special_chars(self, text):
        """
        Further clean text by removing excessive whitespace and special characters if needed.
        """
        # Collapse multiple newlines/spaces
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def split_into_chunks(self, text, metadata=None):
        """
        Split text into overlapping chunks.
        """
        text = self.clean_special_chars(text)
        words = text.split()
        chunks = []
        
        # Simple word-based chunking with overlap
        # chunk_size is number of characters in this implementation for better control
        # Let's switch to character-based chunking for more predictability
        
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Keep original metadata and add chunk-specific info
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata["chunk_start"] = start
            chunk_metadata["chunk_end"] = min(end, len(text))
            
            chunks.append({
                "content": chunk,
                "metadata": chunk_metadata
            })
            
            if end >= len(text):
                break
            
            start += (self.chunk_size - self.overlap)
            
        return chunks

    def process_pages(self, pages):
        """
        Process a list of pages and return all chunks.
        """
        all_chunks = []
        for page in pages:
            logger.info(f"Chunking content from: {page['url']}")
            chunks = self.split_into_chunks(page['content'], metadata={"url": page['url']})
            all_chunks.extend(chunks)
        return all_chunks

if __name__ == "__main__":
    processor = TextProcessor(chunk_size=100, overlap=20)
    sample_text = "This is a long string that we want to split into smaller chunks with some overlap so context is preserved."
    chunks = processor.split_into_chunks(sample_text)
    for i, c in enumerate(chunks):
        print(f"Chunk {i}: {c['content']}")
