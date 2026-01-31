import os
from openai import OpenAI
from storage import VectorStore
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Orchestrates Retrieval Augmented Generation.
    """
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        # Initialize OpenAI client if API key is present
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            logger.warning("OPENAI_API_KEY not found. Answer generation will be mocked.")

    def retrieve(self, query, top_k=3):
        """
        Retrieve relevant chunks for a query.
        """
        results = self.vector_store.search(query, top_k=top_k)
        return results

    def generate_answer(self, query, context_chunks):
        """
        Generate an answer using retrieved context.
        """
        # Prepare context text
        # Since our metadata currently doesn't have the text, I need to fix storage.py
        # For now, let's assume context_chunks have 'content' in metadata (I'll fix storage.py next)
        context_text = "\n\n".join([c['metadata'].get('content', '') for c in context_chunks])
        
        if not context_text:
            return "I'm sorry, I couldn't find any relevant information in the provided website content."

        system_prompt = (
            "You are a helpful support bot. Use ONLY the following context to answer the user's question. "
            "If the answer is not in the context, say 'I don't know based on the provided information'. "
            "Context:\n" + context_text
        )

        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query}
                    ],
                    temperature=0
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                return f"Error generating answer: {str(e)}"
        else:
            return f"[MOCK ANSWER] Based on the context provided, here is what I found: {context_text[:200]}..."

    def ask(self, query):
        """
        Full RAG flow: Retrieve -> Generate.
        """
        context_chunks = self.retrieve(query)
        answer = self.generate_answer(query, context_chunks)
        return {
            "query": query,
            "answer": answer,
            "context": [c['metadata']['url'] for c in context_chunks if 'url' in c['metadata']]
        }
