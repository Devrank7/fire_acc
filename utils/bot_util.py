from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_back_button(index: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data=f"back_{index}")]
    ])
