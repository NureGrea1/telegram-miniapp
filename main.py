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
    # Получаем JSON из запроса
    data = await request.json()
    chat_id = data.get("chat_id")

    if not chat_id:
        return {"message": "chat_id не передан"}

    # Подключаемся к базе данных spy.db
    async with aiosqlite.connect("spy.db") as db:
        # Проверяем, есть ли такой chat_id в таблице spy_messages
        cursor = await db.execute("SELECT 1 FROM spy_messages WHERE chat_id = ? LIMIT 1", (chat_id,))
        result = await cursor.fetchone()

        # Выводим в лог (Render покажет в логах)
        if result:
            print(f"✅ chat_id {chat_id} найден в базе")
            return {"message": f"ID {chat_id} найден ✅"}
        else:
            print(f"❌ chat_id {chat_id} НЕ найден в базе")
            return {"message": f"ID {chat_id} не найден ❌"}
