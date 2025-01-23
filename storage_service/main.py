from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI()

# In-memory storage
game_state: Dict = {}

class PlayerData(BaseModel):
    health: int
    mana: int
    inventory: List[str]
    max_capacity: int
    max_weight: float
    current_weight: float
    gold: int
    experience: int

@app.get("/player/{player_id}")
async def get_player(player_id: str):
    if player_id not in game_state:
        raise HTTPException(status_code=404, detail="Player not found")
    return game_state[player_id]

@app.put("/player/{player_id}")
async def update_player(player_id: str, player_data: PlayerData):
    game_state[player_id] = player_data.dict()
    return {"status": "success"}

@app.delete("/player/{player_id}")
async def delete_player(player_id: str):
    if player_id in game_state:
        del game_state[player_id]
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 