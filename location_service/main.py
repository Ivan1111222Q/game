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
from fastapi import Body

app = FastAPI()




STORAGE_SERVICE = "http://storage-service:8001"



@app.post("/location/lake/{player_id}/action")
async def lake_action(player_id: str,action: dict = Body(...)):
     async with httpx.AsyncClient() as client:
        response = await client.get(f"{STORAGE_SERVICE}/player/{player_id}")
        if response.status_code == 404:
            return {"message": "Игрок не найден", "success": False}

        player_data = response.json()
        item_name = action.get("action")

        
        if item_name == "forward":
            player_data["health"] -= 20
            message = "Вы поплыли прямо и наткнулись на корягу, -20 здоровья."
        elif item_name == "right":
            player_data["mana"] += 10
            message = "Вы поплыли направо и нашли руну, +10 маны."
            if "руна" not in player_data["inventory"]:
                player_data["inventory"].append("руна")
                message += " Руна добавлена в инвентарь!"
        elif item_name == "left":
            if "зелье" in player_data["inventory"]:
                player_data["health"] += 50
                player_data["inventory"].remove("зелье")
                message = "Вы поплыли налево, испили зелье, +50 здоровья. Зелье закончилось."
            else:
                player_data["health"] -= 10
                message = "Вы поплыли налево, но ничего не нашли, -10 здоровья."
        elif item_name == "back":
            player_data["inventory"].append("зелье")
            message = "Вы решили поплыть назад и нашли зелье."
        else:
            return {"message": "Неизвестное направление", "success": False}

        
        if player_data["health"] <= 0:
            message += " Вы погибли от ран, игра окончена!"

        await client.put(f"{STORAGE_SERVICE}/player/{player_id}", json=player_data)

        return {"message": message, "success": True}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)  