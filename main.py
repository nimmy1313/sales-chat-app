from fastapi import FastAPI,WebSocket
from authentication import authentication_router
from my_orders import my_orders_router
from chat_websocket import handle_chat_websocket
from fastapi.middleware.cors import CORSMiddleware
from products import products_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication_router)
app.include_router(my_orders_router)
app.include_router(products_router)

app.mount("/js",StaticFiles(directory="frontend/js"),name="js")

@app.get("/")
async def root():
    return FileResponse("frontend/login.html")

@app.get("/signup")
async def signup():
    return FileResponse("frontend/signup.html")

@app.get("/chat")
async def chat():
    return FileResponse("frontend/chat.html")

@app.get("/login")
async def chat():
    return FileResponse("frontend/login.html")

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket:WebSocket,token:str):
    await handle_chat_websocket(websocket,token)
