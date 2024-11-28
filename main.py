from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import openai
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import pandas as pd

app = FastAPI()
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize processor
from data_processor import DataProcessor
processor = DataProcessor()

# Initialize LangChain
csv_path = "https://docs.google.com/spreadsheets/d/1o0lO6-UfWQAWYz5V7L10X4ooigj44mTvTH3JmqFGB0A/export?format=csv"
# csv_path = 'data/courses.csv'
vectorstore = processor.create_vector_store(csv_path) #'data/courses.csv'
qa_chain = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(temperature=0),
    vectorstore.as_retriever(),
    return_source_documents=True
)

class ChatHistory(BaseModel):
    human: str
    ai: str

class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    chat_history: Optional[List[ChatHistory]] = []

class WebhookRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    chat_history: Optional[List[dict]] = []

@app.post("/query")
async def handle_query(request: QueryRequest):
    try:
        # Convert chat history to format expected by LangChain
        formatted_history = [(msg.human, msg.ai) for msg in request.chat_history] if request.chat_history else []
        
        # Get context from vector store
        result = qa_chain({"question": request.query, "chat_history": formatted_history})
        
        # Format response
        response = {
            "answer": result["answer"],
            "sources": [doc.page_content for doc in result["source_documents"]]
        }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook")
async def handle_webhook(request: WebhookRequest):
    try:
        # Convert webhook request to query request format
        query_request = QueryRequest(
            query=request.message,
            conversation_id=request.conversation_id,
            chat_history=[]  # Initialize empty for now, can be enhanced later
        )
        
        # Process query
        result = await handle_query(query_request)
        
        # Format response for GHL
        ghl_response = {
            "message": result["answer"],
            "conversation_id": request.conversation_id,
            "sources": result["sources"]
        }
        
        return ghl_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)