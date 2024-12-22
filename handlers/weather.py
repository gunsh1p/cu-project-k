from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from utils.api import get_weather
from states import WeatherInput
from keyboards.weather import SKIP_KEYBOARD, INTERVAL_KEYBOARD, get_detailed_link
import config


router = Router(name="weather")
START_TEXT = "Введите начальную точку"
MIDDLE_TEXT = "Введите промежуточную точку:"
END_TEXT = "Введите конечную точку:"
INTERVAL_TEXT = "Выберите временной интервал или введите сами (число от 1 до 5):"
FETCHING_WEATHER_TEXT = "Получение погоды..."

TITLES = {
    0: "Сегодня",
    1: "Завтра",
    2: "Послезавтра",
    3: "Через 3 дня",
    4: "Через 4 дня"
}


@router.message(Command("weather"))
async def cmd_weather(message: Message, state: FSMContext):
    await message.answer(START_TEXT)
    await state.set_state(WeatherInput.start)

@router.message(WeatherInput.start)
async def start_input(message: Message, state: FSMContext):
    city = message.text.strip()
    cities = [city,]
    await message.answer(text=MIDDLE_TEXT, reply_markup=SKIP_KEYBOARD)
    await state.update_data(cities=cities)
    await state.set_state(WeatherInput.middle)

@router.message(WeatherInput.middle)
async def middle_input(message: Message, state: FSMContext):
    city = message.text.strip()
    cities = (await state.get_data())['cities']
    cities.append(city)
    await message.answer(text=MIDDLE_TEXT, reply_markup=SKIP_KEYBOARD)
    await state.update_data(cities=cities)
    await state.set_state(WeatherInput.middle)

@router.callback_query(F.data == "end_point", WeatherInput.middle)
async def end_input(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(END_TEXT)
    await state.set_state(WeatherInput.end)

@router.message(WeatherInput.end)
async def end_input(message: Message, state: FSMContext):
    city = message.text.strip()
    cities = (await state.get_data())['cities']
    cities.append(city)
    text = 'Выбранные точки:\n'
    for i, v in enumerate(cities):
        text += f'{i + 1}. {v}\n'
    await message.answer(text)
    await message.answer(text=INTERVAL_TEXT, reply_markup=INTERVAL_KEYBOARD)
    await state.update_data(cities=cities)
    await state.set_state(WeatherInput.interval)

@router.callback_query(F.data.in_(["three_days", "five_days"]), WeatherInput.interval)
async def interval_select(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(FETCHING_WEATHER_TEXT)
    cities = (await state.get_data())['cities']
    await state.clear()
    interval = 3 if callback.data == "three_days" else 5
    try:
        data = {}
        for city in cities:
            weather = await get_weather(city)
            data[city] = {k: v for k, v in weather['data'].items() if k.startswith("temperature")}
    except Exception:
        await callback.message.edit_text("Произошла ошибка при получении погоды, попробуйте ещё раз")
        return
    text = 'Погода:\n'

    for i in range(interval):
        addition = f"<b>{TITLES[i]}</b>:\n\n"
        addition += "\n".join(f"{k}: {v[f"temperature_{i}"]}°C" for k, v in data.items())
        text += addition + "\n\n"

    await callback.message.edit_text(text=text, reply_markup=get_detailed_link(cities))

@router.message(WeatherInput.interval)
async def interval_input(message: Message, state: FSMContext):
    try:
        interval = int(message.text)
        assert 1 <= interval <= 5
    except ValueError:
        interval = 1
    message = await message.answer(FETCHING_WEATHER_TEXT)
    cities = (await state.get_data())['cities']
    await state.clear()
    try:
        data = {}
        for city in cities:
            weather = await get_weather(city)
            data[city] = {k: v for k, v in weather['data'].items() if k.startswith("temperature")}
    except Exception:
        await message.edit_text("Произошла ошибка при получении погоды, попробуйте ещё раз")
        return
    text = 'Погода:\n'

    for i in range(interval):
        addition = f"<b>{TITLES[i]}</b>:\n\n"
        addition += "\n".join(f"{k}: {v[f"temperature_{i}"]}°C" for k, v in data.items())
        text += addition + "\n\n"

    await message.edit_text(text=text, reply_markup=get_detailed_link(cities))

    
