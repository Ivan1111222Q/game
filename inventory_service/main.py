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
import httpx

app = FastAPI()

STORAGE_SERVICE = "http://storage-service:8001"





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



@app.post("/inventory/{player_id}/use")
async def use_item(player_id: str, item: dict):
    async with httpx.AsyncClient() as client:
        # Получаем данные игрока из storage service
        response = await client.get(f"{STORAGE_SERVICE}/player/{player_id}")
        if response.status_code == 404:
            return {"message": "Игрок не найден", "status": "error"}
        
        player_data = response.json()
        item_name = item.get("item")
        
        if not item_name:
            return {"message": "Предмет не указан", "status": "error"}

        if item_name in player_data["inventory"]:
            if item_name == "зелье":
                player_data["inventory"].remove(item_name)
                player_data["mana"] += 10
                message = f"Предмет '{item_name}' использован, +10% маны."
                success = "success"
            elif item_name == "руна":
                player_data["inventory"].remove(item_name)
                player_data["health"] += 50
                message = f"Предмет '{item_name}' использован, +50 здоровья."
                success = "success"
            elif item_name == "ключ":
                player_data["inventory"].remove(item_name)
                player_data["health"] += 150
                message = f"Предмет '{item_name}' использован, +150 здоровья."
                success = "success"
            else:
                message = f"Предмет '{item_name}' нельзя использовать."
                success = "error"
                
            if success == "success":
                # Обновляем данные в storage service только если были изменения
                await client.put(f"{STORAGE_SERVICE}/player/{player_id}", json=player_data)
        else:
            message = f"Предмет '{item_name}' отсутствует в инвентаре."
            success = "error"

        return {"message": message, "status": success}


@app.post("/inventory/{player_id}/delete")
async def del_inventory(request: Request, player_id: str, item: str = Form(...)):
    async with httpx.AsyncClient() as client:
        # Получаем данные игрока из storage service
        response = await client.get(f"{STORAGE_SERVICE}/player/{player_id}")
        if response.status_code == 404:
            return {"message": "Игрок не найден", "status": "error"}
        
        player_data = response.json()
        if item in player_data["inventory"]:
            player_data["inventory"].remove(item)
            # Обновляем данные в storage service
            await client.put(f"{STORAGE_SERVICE}/player/{player_id}", json=player_data)
            return {"message": f"Предмет {item} удален из инвентаря.", "status": "success"}
        else:
            return {"message": f"Предмет {item} отсутствует в инвентаре.", "status": "error"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)