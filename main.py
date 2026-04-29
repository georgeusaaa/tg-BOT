import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router

load_dotenv()

async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN not found in .env file")
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
