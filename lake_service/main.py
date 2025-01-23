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



@app.get("/lake/{player_id}")
async def lake(request: Request, player_id: str):
    if player_id in game_state:
        player = game_state[player_id]
        return templates.TemplateResponse("lake.html", {"request": request, "player": player})




@app.post("/lake/{player_id}/choice")
async def lake_choice(request: Request, player_id: str, direction: str = Form(...)):
    if player_id not in game_state:
        return RedirectResponse(url="/", status_code=303)

    player = game_state[player_id]
    message = ""
    success = True

    if direction == "forward":
        player["health"] -= 20
        message = "Вы поплыли прямо и наткнулись на корягу, -20 здоровья."
        if player["health"] <= 0:
            if not check_player_health(player_id):
                return templates.TemplateResponse("game_over.html", {"request": request})
            message += " Вы погибли от ран, игра окончена!"
            success = False

    elif direction == "right":
        player["mana"] += 10
        message = "Вы поплыли направо и нашли руну, +10 маны."
        if "руна" not in player["inventory"]:
            player["inventory"].append("руна")
            message += " Руна добавлена в инвентарь!"

    elif direction == "left":
        if "зелье" in player["inventory"]:
            player["health"] += 50
            player["inventory"].remove("зелье")
            message = "Вы поплыли налево, испили зелье, +50 здоровья. Зелье закончилось."
        else:
            player["health"] -= 10
            if not check_player_health(player_id): 
                return templates.TemplateResponse("game_over.html", {"request": request})
            message = "Вы поплыли налево, но ничего не нашли, -10 здоровья."
        
        if player["health"] <= 0:
            if not check_player_health(player_id):  
                return templates.TemplateResponse("game_over.html", {"request": request})
            message += " Вы погибли от ран, игра окончена!"
            success = False

    elif direction == "back":
        player["inventory"].append("зелье")
        message = "Вы решили поплыть назад и нашли зелье."

    else:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse("lake.html", {"request": request,"player": player,"message": message,"success": success})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2000, reload=True)