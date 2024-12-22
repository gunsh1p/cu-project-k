import sys
import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import start, weather
import config


storage = MemoryStorage()
dp = Dispatcher(storage=storage)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s:%(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("bot.log")],
    )

    for logger_name in [
        "httpx",
    ]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)


def setup_routers(dp: Dispatcher):
    dp.include_routers(start.router, weather.router)

async def on_startup(bot: Bot):
    await bot.delete_webhook()

async def main():
    bot = Bot(token=config.TOKEN)

    setup_logging()
    setup_routers(dp)

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
