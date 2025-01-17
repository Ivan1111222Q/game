# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# app = FastAPI()

# # Подключаем папку с шаблонами и статикой
# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Игровое состояние игрока
# player = {
#     "name": "Игрок",
#     "health": 100,
#     "mana": 100,
#     "inventory": []
# }

# # Главная страница
# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request, "player": player})

# # Обработка действий пользователя
# @app.get("/action", response_class=HTMLResponse)
# async def handle_action(request: Request, choice: str):
#     if choice == "lake":
#         return HTMLResponse("<h1>Вы отправились к озеру!</h1><a href='/'>Назад</a>")
#     elif choice == "riddle":
#         return HTMLResponse("<h1>Вот вам загадка: Какого цвета небо? Ответ: голубое</h1><a href='/'>Назад</a>")
#     elif choice == "inventory":
#         inventory = ", ".join(player["inventory"]) if player["inventory"] else "Ваш инвентарь пуст."
#         return HTMLResponse(f"<h1>Инвентарь: {inventory}</h1><a href='/'>Назад</a>")
#     elif choice == "status":
#         return HTMLResponse(
#             f"<h1>Ваши показатели:</h1><p>Здоровье: {player['health']}%</p><p>Мана: {player['mana']}%</p><a href='/'>Назад</a>"
#         )
#     elif choice == "exit":
#         return HTMLResponse("<h1>Вы вышли из игры!</h1>")
#     else:
#         return HTMLResponse("<h1>Неизвестное действие</h1><a href='/'>Назад</a>")



from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

class Player(BaseModel):
    name: str = "Игрок"
    health: int = 100
    mana: int = 100
    inventory: list[str] = []

def initialize_player():
    return Player(name="Игрок", health=100, mana=100, inventory=[])

player = initialize_player()

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Magical Forest Adventure</title>
</head>
<body>
    <h1>Добро пожаловать в Магический Лес, {{ player.name }}!</h1>
    <h2>Показатели Игрока:</h2>
    <p>Здоровье: {{ player.health }}%</p>
    <p>Мана: {{ player.mana }}%</p>
    <p>Инвентарь: {{ ', '.join(player.inventory) if player.inventory else 'пусто' }}</p>
    <h3>Выберите действие:</h3>
    <form action="/action" method="post">
        <input type="radio" name="action" value="1"> Отправиться к озеру<br>
        <input type="radio" name="action" value="2"> Разгадать загадку<br>
        <input type="radio" name="action" value="3"> Открыть инвентарь<br>
        <input type="radio" name="action" value="4"> Показатели игрока<br>
        <input type="radio" name="action" value="5"> Выйти из игры<br>
        <br>
        <input type="submit" value="Применить">
    </form>
</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(content=html_template.replace("{{ player.name }}", player.name)
                        .replace("{{ player.health }}", str(player.health))
                        .replace("{{ player.mana }}", str(player.mana))
                        .replace("{{ ', '.join(player.inventory) if player.inventory else 'пусто' }}", ", ".join(player.inventory) if player.inventory else "пусто"))

@app.post("/action")
async def action(request: Request):
    form_data = await request.form()
    action = form_data["action"]

    if action == "1":  # Отправиться к озеру
        player.health -= 5
        return HTMLResponse(content=f"Вы остаетесь на берегу, ваше здоровье уменьшилось на 5%. <a href='/'>Назад</a>")
    elif action == "2":  # Разгадать загадку
        riddles = {
            'Цвет небо': 'голубое',
            'Какой огонь': 'горячий'
        }
        riddle, answer = random.choice(list(riddles.items()))
        return HTMLResponse(content=f'<h2>Разгадайте загадку: {riddle}</h2>'
                                    f'<form action="/riddle" method="post">'
                                    f'<input type="text" name="answer" placeholder="Введите ваш ответ">'
                                    f'<input type="submit" value="Ответить">'
                                    f'</form>')
    elif action == "3":  # Открыть инвентарь
        return HTMLResponse(content=f"Инвентарь: {', '.join(player.inventory) if player.inventory else 'пусто'}<br>"
                                    f"<form action='/inventory' method='post'>"
                                    f"<input type='submit' value='Выйти'>"
                                    f"</form>")
    elif action == "4":  # Показатели игрока
        return HTMLResponse(content=f"Здоровье: {player.health}%<br>"
                                    f"Мана: {player.mana}%<br>"
                                    f"<form action='/inventory' method='post'>"
                                    f"<input type='submit' value='Назад'>"
                                    f"</form>")
    elif action == "5":  # Выйти из игры
        return HTMLResponse(content="Выход из игры!")

    return HTMLResponse(content="Произошла ошибка. Пожалуйста, попробуйте снова.")

@app.post("/riddle")
async def riddle(request: Request):
    form_data = await request.form()
    user_answer = form_data["answer"].strip().lower()
    riddles = {
        'Цвет небо': 'голубое',
        'Какой огонь': 'горячий'
    }
    riddle, answer = random.choice(list(riddles.items()))

    if user_answer == answer:
        player.health += 10
        return HTMLResponse(content=f"Вы угадали! Здоровье увеличилось на 10%. <a href='/'>Назад</a>")
    else:
        player.health -= 50
        return HTMLResponse(content=f"Вы не угадали! Здоровье уменьшилось на 50%. <a href='/'>Назад</a>")

@app.post("/inventory")
async def inventory(request: Request):
    return HTMLResponse(content=f"Инвентарь: {', '.join(player.inventory) if player.inventory else 'пусто'}<br>"
                                f"<form action='/action' method='post'>"
                                f"<input type='submit' value='Назад'>"
                                f"</form>")
