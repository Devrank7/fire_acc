from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

router = Router()

start_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать аккаунт", callback_data="create_acc")],
    [InlineKeyboardButton(text="Мои аккаунты", callback_data="my_acc")],
])


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    text = "Выберете действе: "
    await state.update_data(bt0=text)
    await state.update_data(br0=start_button)
    await message.answer(text, reply_markup=start_button)
