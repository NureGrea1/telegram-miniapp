from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import aiosqlite

app = FastAPI()

# Разрешаем доступ с фронта на Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://telegram-miniapp-plum.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)
#test
@app.post("/auth")
async def auth_user(request: Request):
    data = await request.json()
    chat_id = data["id"]
    chat_username = data.get("username", "без ника")

    async with aiosqlite.connect("spy_notifications") as db:
        # Создаем таблицу, если ее нет (можно убрать, если она уже есть)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS spy_notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_connection_id TEXT NOT NULL,
                business_user_id INTEGER NOT NULL,
                business_username TEXT,
                chat_id INTEGER NOT NULL,
                chat_username TEXT,
                notification_type TEXT NOT NULL,
                message_id INTEGER NOT NULL,
                old_text TEXT,
                new_text TEXT,
                message_type TEXT,
                media_file_id TEXT,
                from_id INTEGER NOT NULL,
                from_first_name TEXT NOT NULL,
                from_username TEXT,
                notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.commit()

        # Проверяем наличие пользователя по chat_id
        cursor = await db.execute("""
            SELECT chat_username FROM spy_notifications WHERE chat_id = ?
        """, (chat_id,))
        row = await cursor.fetchone()

        if not row:
            # Добавляем тестовую строку (с минимальными обязательными полями)
            await db.execute("""
                INSERT INTO spy_notifications (
                    business_connection_id, business_user_id, business_username,
                    chat_id, chat_username, notification_type, message_id,
                    from_id, from_first_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                "connection_1", 1, "demo_user",
                chat_id, chat_username, "login", 1,
                chat_id, "TelegramUser"
            ))
            await db.commit()
            return {"message": f"Привет, {chat_username}! Ты добавлен в базу."}
        else:
            return {"message": f"Привет снова, {row[0]}!"}
