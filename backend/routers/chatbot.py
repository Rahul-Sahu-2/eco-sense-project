from fastapi import APIRouter
from pydantic import BaseModel

from backend.services import groq_service

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])


class ChatRequest(BaseModel):
    message: str


@router.post("")
async def chat(req: ChatRequest):
    response = groq_service.chat_response(req.message)
    return {"response": response}
