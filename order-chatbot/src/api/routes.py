from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict

from src.chatbot.chain import create_chatbot_chain

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    customer_id: Optional[int] = None
    context: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    context: Dict

@app.get("/")
async def root():
    return {"status": "Chatbot API is running"}

@app.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        # Tạo chatbot chain
        components = create_chatbot_chain(request.customer_id)
        chatbot = components["chain"]
        
        # Xử lý tin nhắn
        response, new_context = chatbot.generate_response(
            request.message,
            request.context
        )
        
        return ChatResponse(
            response=response,
            context=new_context
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 