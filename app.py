from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import RAGPipeline
from storage import VectorStore
import logging

app = FastAPI(title="RAG Q&A Bot API")
logger = logging.getLogger(__name__)

# Initialize dependencies
# In a real app, you might use lifespan events or dependency injection
vector_store = VectorStore()
# We assume the index is already built or will be built before queries
pipeline = RAGPipeline(vector_store)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    context: list

@app.get("/")
def read_root():
    return {"message": "RAG Q&A Bot is running. Use /ask to query."}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    """
    Endpoint to ask a question to the RAG bot.
    """
    try:
        logger.info(f"Received question: {request.question}")
        result = pipeline.ask(request.question)
        return result
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
