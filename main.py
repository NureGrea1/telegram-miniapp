from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import aiosqlite

app = FastAPI()

# Разрешаем фронту (с Vercel) обращаться к нашему серверу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://telegram-miniapp-2pys.vercel.app"],  # Замени на свой домен
    allow_methods=["*"],
    allow_headers=["*"],
)

# POST-запрос на /check
@app.post("/check")
async def check_chat_id(request: Request):
    
    data = await request.json()
    chat_id = data.get("chat_id")

    if chat_id == 640055320:
        return {"message": f"ID {chat_id} найден ✅"}
    else:
        return {"message": f"ID {chat_id} не найден ❌"}
