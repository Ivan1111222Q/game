from fastapi import FastAPI, Body
import uvicorn
import httpx

app = FastAPI()

STORAGE_SERVICE = "http://storage-service:8001"

@app.get("/location/lake")
async def get_lake_info():
    return {
        "name": "Озеро",
        "description": "Вы находитесь у таинственного озера. Куда поплывете?",
        "options": ["forward", "right", "left", "back"]
    }

@app.post("/location/lake/{player_id}/action")
async def lake_choice(player_id: str, action: dict = Body(...)):
    async with httpx.AsyncClient() as client:
        # Получаем данные игрока из storage service
        response = await client.get(f"{STORAGE_SERVICE}/player/{player_id}")
        if response.status_code == 404:
            return {"message": "Игрок не найден", "success": False}
        
        player_data = response.json()
        message = ""
        success = True
        direction = action.get("action")

        if direction == "forward":
            player_data["health"] -= 20
            message = "Вы поплыли прямо и наткнулись на корягу, -20 здоровья."
            if player_data["health"] <= 0:
                message += " Вы погибли от ран, игра окончена!"
                success = False

        elif direction == "right":
            player_data["mana"] += 10
            message = "Вы поплыли направо и нашли руну, +10 маны."
            if "руна" not in player_data["inventory"]:
                player_data["inventory"].append("руна")
                message += " Руна добавлена в инвентарь!"

        elif direction == "left":
            if "зелье" in player_data["inventory"]:
                player_data["health"] += 50
                player_data["inventory"].remove("зелье")
                message = "Вы поплыли налево, испили зелье, +50 здоровья. Зелье закончилось."
            else:
                player_data["health"] -= 10
                message = "Вы поплыли налево, но ничего не нашли, -10 здоровья."
            
            if player_data["health"] <= 0:
                message += " Вы погибли от ран, игра окончена!"
                success = False

        elif direction == "back":
            player_data["inventory"].append("зелье")
            message = "Вы решили поплыть назад и нашли зелье."

        else:
            return {"message": "Неверное направление", "success": False}

        # Обновляем данные игрока только если он жив
        if player_data["health"] > 0:
            await client.put(f"{STORAGE_SERVICE}/player/{player_id}", json=player_data)

        return {"message": message, "success": success}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004) 