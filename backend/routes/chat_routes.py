from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from models.chat_model import ChatModel

router = APIRouter()
chat_model = ChatModel()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    confidence: float = 1.0

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint for AI Assistant"""
    try:
        logger.info(f"Chat request: {request.message[:50]}...")
        
        if not request.message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        reply = await chat_model.get_response(request.message)
        
        return ChatResponse(reply=reply, confidence=1.0)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history")
async def get_chat_history():
    """Get chat history (for future enhancement)"""
    return {"history": []}