from fastapi import APIRouter, HTTPException, Depends
from app.services.chat_service import ChatService
from pydantic import BaseModel
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def get_recommendations(request: ChatRequest):
    try:
        print(f"Recibido mensaje: {request.message}")  # Debug
        result = await chat_service.get_movie_recommendations(request.message)
        return result
    except Exception as e:
        print(f"Error en chat endpoint: {str(e)}")  # Debug
        raise HTTPException(status_code=500, detail=str(e)) 