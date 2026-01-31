import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
import pickle
import os

logger = logging.getLogger(__name__)

class VectorStore:
    """
    Handles embeddings generation and FAISS vector storage.
    """
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path="faiss_index.bin", metadata_path="metadata.pkl"):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = []

    def create_index(self, chunks):
        """
        Create a FAISS index from text chunks.
        """
        if not chunks:
            logger.warning("No chunks provided to create index.")
            return

        texts = [c['content'] for c in chunks]
        # Include content in metadata for retrieval
        self.metadata = []
        for c in chunks:
            meta = c['metadata'].copy()
            meta['content'] = c['content']
            self.metadata.append(meta)
        
        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        
        logger.info("FAISS index created successfully.")
        self.save()

    def save(self):
        """
        Save the index and metadata to disk.
        """
        if self.index:
            faiss.write_index(self.index, self.index_path)
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.metadata, f)
            logger.info(f"Index and metadata saved to {self.index_path} and {self.metadata_path}")

    def load(self):
        """
        Load the index and metadata from disk.
        """
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            logger.info("Index and metadata loaded successfully.")
            return True
        return False

    def search(self, query, top_k=3):
        """
        Perform similarity search.
        """
        if self.index is None:
            if not self.load():
                logger.error("Index not initialized or loaded.")
                return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1: # FAISS returns -1 if not enough results
                # We need to store the original text too if we want to retrieve it.
                # Let's modify the metadata to include the content during creation.
                results.append({
                    "metadata": self.metadata[idx],
                    "distance": float(distances[0][i])
                })
        return results

# Note: To return text content, we should store it in metadata or a separate mapping.
# Let's adjust VectorStore.create_index to ensure metadata includes text.
