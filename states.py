from aiogram.fsm.state import State, StatesGroup


class WeatherInput(StatesGroup):
    start = State()
    middle = State()
    end = State()
    interval = State()
