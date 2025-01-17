# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import random
# import uvicorn

# app = FastAPI()

# @app.get("/start")
# async def start(request: Request):
#     player = initialize_player()
#     p = 'Добро пожаловать в Магический Лес!'
#     actions = {
#         '1': 'Отправиться к озеру',
#         '2': 'Разгадать загадку',
#         '3': 'Открыть инвентарь',
#         '4': 'Показатели игрока',
#         '5': 'Выйти из игры!'
#     }
#     return actions, p




# def initialize_player():
#     player_id = str(random.randint(1000, 9999))
#     player = {
#         'health': 100,
#         'mana': 100,
#         'inventory': [],
#         'player_id': player_id
#     }
#     return player


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Подключаем папку с шаблонами и статикой
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Игровое состояние игрока
player = {
    "name": "Игрок",
    "health": 100,
    "mana": 100,
    "inventory": []
}

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "player": player})

# Обработка действий пользователя
@app.get("/action", response_class=HTMLResponse)
async def handle_action(request: Request, choice: str):
    if choice == "lake":
        return HTMLResponse("<h1>Вы отправились к озеру!</h1><a href='/'>Назад</a>")
    elif choice == "riddle":
        return HTMLResponse("<h1>Вот вам загадка: Какого цвета небо? Ответ: голубое</h1><a href='/'>Назад</a>")
    elif choice == "inventory":
        inventory = ", ".join(player["inventory"]) if player["inventory"] else "Ваш инвентарь пуст."
        return HTMLResponse(f"<h1>Инвентарь: {inventory}</h1><a href='/'>Назад</a>")
    elif choice == "status":
        return HTMLResponse(
                            f"<h1>Здоровье: {player['health']}%</h1>"
                            f"<h1>Мана: {player['mana']}%</h1>"
                            f"<h1>Инвентарь: {', '.join(player['inventory']) if player['inventory'] else 'пусто'}</h1>"
                            f"<h1><a href='/'>Назад</a></h1>"
                            f"<form method='POST' action='/your_action'>"
                            f"    <input type='submit' value='Ответить' />"
                            f"<form action='/inventory' method='post' />"
                            f"</form>"
                            )
    elif choice == "exit":
        return HTMLResponse("<h1>Вы вышли из игры!</h1>")
    else:
        return HTMLResponse("<h1>Неизвестное действие</h1><a href='/'>Назад</a>")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2000, reload=True)