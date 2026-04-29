import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout
from handlers import router


async def main():
    session = AiohttpSession(timeout=ClientTimeout(total=30))
    bot = Bot(token="", session=session)
    dp = Dispatcher()
    dp.include_router(router)


    for attempt in range(3):
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            print(f"✓ Бот запущен! Попытка {attempt + 1}")
            await dp.start_polling(bot)
            break
        except Exception as e:
            print(f"✗ Ошибка (попытка {attempt + 1}): {e}")
            if attempt < 2:
                print(f"Повтор через 5 секунд...")
                await asyncio.sleep(5)
            else:
                print("Не удалось подключиться. Проверьте интернет и VPN.")
                raise


if __name__ == "__main__":
    asyncio.run(main())