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



@app.get("/")
async def read_root(request: Request, player_id: Optional[str] = Cookie(None)):
    if player_id and player_id in game_state:
        return RedirectResponse(url=f"/game/{player_id}")
    response = templates.TemplateResponse("index.html", {"request": request})
    return response 




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


   

@app.get("/inventory/{player_id}/")
async def get_inventory(request: Request, player_id: str, message: str = None, success: bool = None):
    if player_id in game_state:
        player = game_state[player_id]
        return templates.TemplateResponse("inventory.html", {"request": request, "player": player, "message": message, "success": success})
    return RedirectResponse(url="/", status_code=303)


@app.get("/lake/{player_id}")
async def lake(request: Request, player_id: str):
    if player_id in game_state:
        player = game_state[player_id]
        return templates.TemplateResponse("lake.html", {"request": request, "player": player})
    


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