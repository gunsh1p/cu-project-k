from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command


router = Router(name="start-and-help")


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот для получения прогноза погоды. Используйте /help для получения списка команд.")

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - помощь\n"
        "/weather - прогноз погоды"
    )
    await message.answer(text)
