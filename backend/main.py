import os
from dotenv import load_dotenv   # type: ignore
from llm import llmChatService # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi import FastAPI, HTTPException, Depends # type: ignore
from models import ChatRequest, ChatResponse, Message

# Load environment variables at the very top
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

def get_llm_service() -> llmChatService:
    return llmChatService()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    llm_service: llmChatService = Depends(get_llm_service) 
):
    try:
        gemini_response_text = await llm_service.get_chat_response(
            user_message=request.message,
            chat_history=request.history
        )
        return ChatResponse(response=gemini_response_text)

    except Exception as e:
        print(f"An error occurred in chat_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error communicating with LLM.")

@app.get("/")
async def read_root():
    return {"message": "Travel Buddy Chatbot Backend is running with Gemini!"}