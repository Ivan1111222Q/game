from fastapi import FastAPI, Request, HTTPException, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
from typing import Optional
import random
from fastapi import Body

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Конфигурация сервисов
SERVICES = {
    "storage": "http://storage-service:8001",
    "inventory": "http://inventory-service:8002",
    "riddle": "http://riddle-service:8003",
    "location": "http://location-service:8004"
}

# ridle_service 
# riddles = [
#     {"id": "1", "text": "Цвет неба", "answer": "голубое"},
#     {"id": "2", "text": "Какой огонь", "answer": "горячий"}
# ]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, player_id: Optional[str] = Cookie(None)):
    if player_id:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{SERVICES['storage']}/player/{player_id}")
                if response.status_code == 200:
                    return RedirectResponse(url=f"/game/{player_id}")
            except:
                pass
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start")
async def start_game():
    player_id = str(random.randint(1000, 9999))
    player_data = {
        "health": 100,
        "mana": 100,
        "inventory": ['ключ'],
        "max_capacity": 10,
        "max_weight": 10.0,
        "current_weight": 0.0,
        "gold": 0,
        "experience": 0
    }
    
    async with httpx.AsyncClient() as client:
        await client.put(f"{SERVICES['storage']}/player/{player_id}", json=player_data)
    
    response = RedirectResponse(url=f"/game/{player_id}", status_code=303)
    response.set_cookie(key="player_id", value=player_id, max_age=3600)
    return response

@app.get("/game/{player_id}")
async def get_game(request: Request, player_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['storage']}/player/{player_id}")
        if response.status_code == 404:
            return RedirectResponse(url="/")
        player_data = response.json()
        player_data['player_id'] = player_id
        return templates.TemplateResponse("game.html", {
            "request": request,
            "player": player_data
        })

@app.get("/inventory/{player_id}")
async def get_inventory(request: Request, player_id: str, message: str = None, success: bool = None):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['storage']}/player/{player_id}")
        if response.status_code == 404:
            return RedirectResponse(url="/")
        player_data = response.json()
        player_data['player_id'] = player_id
        return templates.TemplateResponse("inventory.html", {
            "request": request,
            "player": player_data,
            "message": message,
            "success": success
        })


@app.post("/inventory/{player_id}/use")
async def use_item(player_id: str, item: str = Form(...)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SERVICES['inventory']}/inventory/{player_id}/use",
            json={"item": item}
        )
        try:
            result = response.json()
        except Exception as e:
            print(f"Ошибка при разборе JSON: {e}")
            return RedirectResponse(
                url=f"/inventory/{player_id}?message=Ошибка сервиса&success=false",
                status_code=303
            )

        return RedirectResponse(
            url=f"/inventory/{player_id}?message={result['message']}&success={result['status'] == 'success'}",
            status_code=303
        )


@app.post("/inventory/{player_id}/delete")
async def delete_item(player_id: str, item: str = Form(...)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SERVICES['inventory']}/inventory/{player_id}/delete",
            data={"item": item}
        )
        result = response.json()
        return RedirectResponse(
            url=f"/inventory/{player_id}?message={result['message']}&success={result['status'] == 'success'}",
            status_code=303
        )


@app.get("/lake/{player_id}")
async def get_lake(request: Request, player_id: str, message: str = None, success: bool = None):
    async with httpx.AsyncClient() as client:
        # Получаем данные игрока
        response = await client.get(f"{SERVICES['storage']}/player/{player_id}")
        if response.status_code == 404:
            return RedirectResponse(url="/")
        player_data = response.json()
        player_data['player_id'] = player_id  # Добавляем player_id в данные
        
        return templates.TemplateResponse("lake.html", {
            "request": request,
            "player": player_data,
            "message": message,
            "success": success
        })

@app.post("/lake/{player_id}/choice")
async def lake_choice(player_id: str, direction: str = Form(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{SERVICES['location']}/location/lake/{player_id}/action",
                json={"action": direction}
            )
            result = response.json()
            
            # Если игрок погиб, получаем его данные для отображения game_over
            if not result["success"] and "погибли" in result["message"]:
                player_response = await client.get(f"{SERVICES['storage']}/player/{player_id}")
                if player_response.status_code == 200:
                    player_data = player_response.json()
                    return templates.TemplateResponse("game_over.html", {
                        "request": Request,
                        "player": player_data,
                        "message": result["message"]
                    })
                
            return RedirectResponse(
                url=f"/lake/{player_id}?message={result['message']}&success={result['success']}",
                status_code=303
            )
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            return RedirectResponse(
                url=f"/lake/{player_id}?message=Произошла ошибка&success=false",
                status_code=303
            )



@app.get("/riddle/{player_id}")
async def get_lake(request: Request, player_id: str, message: str = None, success: bool = None):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICES['storage']}/player/{player_id}")
        if response.status_code == 404:
            return RedirectResponse(url="/")
        player_data = response.json()
        player_data['player_id'] = player_id

        response = await client.get(f"{SERVICES['riddle']}/riddle/get_riddle")
        response = response.json()

    
        riddle = response['riddle']


        
        return templates.TemplateResponse("riddle.html", {
            "request": request,
            "player": player_data,
            "riddle": riddle,
            "message": message,
            "success": success
        })




@app.post("/riddle/{player_id}/answer")
async def answer_riddle(request: Request, player_id: str, riddle_id: str = Form(...), answer: str = Form(...)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVICES['riddle']}/riddle/{player_id}/check",
                              json={"riddle_id": riddle_id, "answer": answer},
                                        )
            result = response.json()


            if not result["success"] and "погибли" in result["message"]:
             player_response = await client.get(f"{SERVICES['storage']}/player/{player_id}")
             if player_response.status_code != 200:
               player_data = player_response.json()
               return templates.TemplateResponse("game_over.html", {
                        "request": Request,
                        "player": player_data,
                        "message": result["message"]
                    })


            return RedirectResponse(
                url=f"/riddle/{player_id}?message={result['message']}&success={result['success']}",
                status_code=303
            )
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            return RedirectResponse(
                url=f"/riddle/{player_id}?message=Произошла ошибка&success=false",
                status_code=303
            )




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)    