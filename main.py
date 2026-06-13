import asyncio
import os
from aiogram import Bot, Dispatcher
from bot.handlers import chat, admin

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(chat.router)
    dp.include_router(admin.router)
    print("JoroChatBot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
