from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

@app.get("/auth_service/{endpoint}")
async def proxy_to_app1(endpoint: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://auth_service:5000/{endpoint}")
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/game_service/{endpoint}")
async def proxy_to_app2(endpoint: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://game_service:5000/{endpoint}")
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    

@app.get("/inventory_service/{endpoint}")
async def proxy_to_app3(endpoint: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://inventory_service:5000/{endpoint}")
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    
@app.get("/riddle_service/{endpoint}")
async def proxy_to_app4(endpoint: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://riddle_service:5000/{endpoint}")
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

