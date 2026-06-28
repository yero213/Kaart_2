from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Pydantic schema voor data-validatie
class GameStartRequest(BaseModel):
    player_names: List[str]

@router.get("/api/status")
async def get_status():
    """
    Controleert of de backend online is.
    """
    return {
        "status": "healthy",
        "game": "kleurenwiezen",
        "version": "1.0.0"
    }

@router.post("/api/game/start")
async def start_game(request: GameStartRequest):
    """
    Start een nieuw spelletje Kleurenwiezen met minimaal 4 spelers.
    """
    if len(request.player_names) < 4:
        return {"error": "Kleurenwiezen vereist minimaal 4 spelers."}
        
    return {
        "message": "Spel succesvol gestart!",
        "players": request.player_names,
        "dealer": request.player_names[0]
    }