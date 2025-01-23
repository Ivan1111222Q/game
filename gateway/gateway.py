from fastapi import FastAPI, HTTPException
import httpx
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

@app.get("/lake_service/{endpoint}")
async def proxy_to_app5(endpoint: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://lake_service:5000/{endpoint}")
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)    