from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

