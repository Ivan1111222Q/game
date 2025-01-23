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





@app.get("/inventory/{player_id}/")
async def get_inventory(request: Request, player_id: str, message: str = None, success: bool = None):
    if player_id in game_state:
        player = game_state[player_id]
        return templates.TemplateResponse("inventory.html", {"request": request, "player": player, "message": message, "success": success})
    return RedirectResponse(url="/", status_code=303)



@app.post("/inventory/{player_id}/use")
async def use_item(request: Request, player_id: str, item: str = Form(...)):
    if player_id in game_state:
        player = game_state[player_id]

        if item in player["inventory"]:
            if item == "зелье":
                player["inventory"].remove(item)
                player["mana"] += 10
                message = f"Предмет '{item}' использован, +10% маны."
                success = True
            elif item == "руна":
                player["inventory"].remove(item)
                player["health"] += 50
                message = f"Предмет '{item}' использован, +50 здоровья."
                success = True
            elif item == "ключ":
                player["inventory"].remove(item)
                player["health"] += 150
                message = f"Предмет '{item}' использован, +150 здоровья."
                success = True
            else:
                message = f"Предмет '{item}' нельзя использовать."
                success = False                
        else:
            message = f"Предмет '{item}' отсутствует в инвентаре."
            success = False

        return RedirectResponse(
            url=f"/inventory/{player_id}?message={message}&success={success}",
            status_code=303
        )

    return RedirectResponse(url="/", status_code=303)


@app.post("/inventory/{player_id}/delete")
async def del_inventory(request: Request, player_id: str, item: str = Form(...)):
    if player_id in game_state:
        player = game_state[player_id]
        if item in player["inventory"]:
            player["inventory"].remove(item)
            message = f"Предмет {item} удален из инвентаря."
            success = False
        else:
            message = f"Предмет {item} отсутствует в инвентаре."
            success = False

        return RedirectResponse(
             url=f"/inventory/{player_id}?message={message}&success={success}",
             status_code=303
         )

    return templates.TemplateResponse("inventory.html", {"request": request,"player": player,"message": message,"success": success})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2000, reload=True)