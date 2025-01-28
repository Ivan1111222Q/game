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


@app.post("/riddle/{player_id}/check")
async def answer_riddle(
    request: Request, player_id: str, riddle_id: str = Form(...), answer: str = Form(...)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{STORAGE_SERVICE['storage']}/player/{player_id}")
        if response.status_code == 404:
            return RedirectResponse(
                url=f"/?message=Игрок не найден&success=False", status_code=303
            )

        player_data = response.json()

        riddles = {
            "1": {"question": "Цвет неба", "answer": "голубое"},
            "2": {"question": "Какой огонь", "answer": "горячий"},
        }

        riddle = riddles.get(riddle_id)
        if not riddle:
            return {"message": message, "success": True}

        # Проверка ответа
        if answer.lower() == riddle["answer"].lower():
            # Успешный ответ: добавляем "ключ" в инвентарь
            player_data["inventory"].append("ключ")
            message = "Правильный ответ! Предмет 'ключ' добавлен в инвентарь."
            success = True
        else:
            # Неправильный ответ: уменьшаем здоровье
            player_data["health"] -= 50
            message = "Неправильный ответ. Попробуйте снова."
            success = False

        # Редирект обратно к загадке
        return {"message": message, "success": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003) 