from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

router = Router()

start_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать аккаунт", callback_data="create_acc")],
    [InlineKeyboardButton(text="Мои аккаунты", callback_data="my_acc")],
])


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Выберете действе: ", reply_markup=start_button)
