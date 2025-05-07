from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "my_acc")
async def my(query: CallbackQuery):
    pass