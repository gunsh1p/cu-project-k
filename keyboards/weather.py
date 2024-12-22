from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config

SKIP_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ввести конечную точку", callback_data="end_point")
        ]
    ]
)

INTERVAL_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="На 3 дня", callback_data="three_days")
        ],
        [
            InlineKeyboardButton(text="На 5 дней", callback_data="five_days")
        ]
    ]
)

def get_detailed_link(cities: list[str]) -> InlineKeyboardMarkup:
    query_params = '&'.join(f"city={city}" for city in cities)
    url = config.API_HOST + f"/details?{query_params}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Детальная информация", url=url)
            ]
        ]
    )
