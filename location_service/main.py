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
async def lake_action(player_id: str, action: dict = Body(...)):
    async with httpx.AsyncClient() as client:
        # Получаем данные игрока из storage service
        response = await client.get(f"{STORAGE_SERVICE}/player/{player_id}")
        if response.status_code == 404:
            return {"message": "Игрок не найден", "success": False}
        
        player_data = response.json()
   





# @app.post("/lake/{player_id}/choice")
# async def lake_choice(request: Request, player_id: str, direction: str = Form(...)):
#    async with httpx.AsyncClient() as client:
#         # Получаем данные игрока из storage service
#         response = await client.get(f"{STORAGE_SERVICE}/player/{player_id}")
#         if response.status_code == 404:
#             return {"message": "Игрок не найден", "status": "error"}

#     player = game_state[player_id]
#     message = ""
#     success = True

#     if direction == "forward":
#         player["health"] -= 20
#         message = "Вы поплыли прямо и наткнулись на корягу, -20 здоровья."
#         if player["health"] <= 0:
#             if not check_player_health(player_id):
#                 return templates.TemplateResponse("game_over.html", {"request": request})
#             message += " Вы погибли от ран, игра окончена!"
#             success = False

#     elif direction == "right":
#         player["mana"] += 10
#         message = "Вы поплыли направо и нашли руну, +10 маны."
#         if "руна" not in player["inventory"]:
#             player["inventory"].append("руна")
#             message += " Руна добавлена в инвентарь!"

#     elif direction == "left":
#         if "зелье" in player["inventory"]:
#             player["health"] += 50
#             player["inventory"].remove("зелье")
#             message = "Вы поплыли налево, испили зелье, +50 здоровья. Зелье закончилось."
#         else:
#             player["health"] -= 10
#             if not check_player_health(player_id): 
#                 return templates.TemplateResponse("game_over.html", {"request": request})
#             message = "Вы поплыли налево, но ничего не нашли, -10 здоровья."
        
#         if player["health"] <= 0:
#             if not check_player_health(player_id):  
#                 return templates.TemplateResponse("game_over.html", {"request": request})
#             message += " Вы погибли от ран, игра окончена!"
#             success = False

#     elif direction == "back":
#         player["inventory"].append("зелье")
#         message = "Вы решили поплыть назад и нашли зелье."

#     else:
#         return RedirectResponse(url="/", status_code=303)

#     return templates.TemplateResponse("lake.html", {"request": request,"player": player,"message": message,"success": success})



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004) 