from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import random
from fastapi.responses import RedirectResponse
from fastapi import Cookie
from typing import Optional
from fastapi import Form

app = FastAPI()


templates = Jinja2Templates(directory="templates")


game_state = {}



item = {
    "id": "health_potion",
    "name": "Зелье здоровья",
    "category": "potion",
    "weight": 0.5,
    "rarity": "common",
    "quantity": 1,
    "effects": {"health": 50}
}




def initialize_player(player_id):
    player = {
        "health": 100,
        "mana": 100,
        "inventory": [],
        "max_capacity": 10,
        "max_weight": 10.0,
        "current_weight": 0.0,
        "player_id": player_id,
        "gold": 0,
        "experience": 0
    }
    return player


def add_to_inventory(player_id: str, item: str):
    if player_id in game_state:
       game_state[player_id]['inventory'].append(item)
       return True
    return False

def check_player_health(player_id: str) -> bool:
  
    if player_id in game_state:
        player = game_state[player_id]
        if player["health"] <= 0:
            del game_state[player_id]  
            return False
    return True



@app.post("/start")
async def start_game():
    player_id = str(random.randint(1000, 9999))
    game_state[player_id] = initialize_player(player_id)
    response = RedirectResponse(url=f"/game/{player_id}", status_code=303)
    response.set_cookie(
        key="player_id",
        value=player_id,
        max_age=3600,
        httponly=True,
        samesite='lax'
    )
    return response


@app.get("/game/{player_id}")
async def game(request: Request, player_id: str, stored_player_id: Optional[str] = Cookie(None)):
    # Если игрока нет в game_state - на главную
    if player_id not in game_state:
        response = RedirectResponse(url="/", status_code=303)
        response.delete_cookie(key="player_id", path="/")
        return response
    
    # Если нет куки или она не совпадает, но игрок существует - устанавливаем куки
    if (not stored_player_id or stored_player_id != player_id) and player_id in game_state:
        response = templates.TemplateResponse("game.html", {
            "request": request,
            "player": game_state[player_id]
        })
        response.set_cookie(key="player_id", value=player_id, max_age=3600)
        response.headers.update({
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        })
        return response
    
    response = templates.TemplateResponse("game.html", {
        "request": request,
        "player": game_state[player_id]
    })
    response.headers.update({
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    })
    return response   


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2000, reload=True)