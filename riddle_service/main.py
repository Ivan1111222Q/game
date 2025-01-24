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


templates = Jinja2Templates(directory="gateway/templates")


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



@app.post("/riddle/{player_id}/answer")
async def answer_riddle(request: Request, player_id: str, riddle_id: str = Form(...), answer: str = Form(...)):
    riddles = {
        "1": {"question": "Цвет неба", "answer": "голубое"},
        "2": {"question": "Какой огонь", "answer": "горячий"}
    }

    if player_id in game_state:
        player = game_state[player_id]

        riddle = riddles.get(riddle_id)
        if not riddle:
            return RedirectResponse(url=f"/game/{player_id}?message=Загадка не найдена&success=False", status_code=303)

        if answer.lower() == riddle["answer"].lower():
            player["inventory"].append("ключ")
            message = "Правильный ответ! Предмет 'ключ' добавлен в инвентарь."
            success = True
        else:
            player["health"] -= 50
            if not check_player_health(player_id): 
                return templates.TemplateResponse("game_over.html", {"request": request})
            message = "Неправильный ответ. Попробуйте снова."
            success = False

        return RedirectResponse(url=f"/riddle/{player_id}?message={message}&success={success}", status_code=303)
    




@app.get("/riddle/{player_id}")
async def riddle(request: Request, player_id: str, message: str = None, success: bool = None):
    riddles = [
        {"id": "1", "text": "Цвет неба", "answer": "голубое"},
        {"id": "2", "text": "Какой огонь", "answer": "горячий"}
    ]

    if player_id in game_state:
        player = game_state[player_id]
        riddle = random.choice(riddles)

        return templates.TemplateResponse(
            "riddle.html",{"request": request,"player": player,"riddle": riddle,"message": message,"success": success,},)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003) 