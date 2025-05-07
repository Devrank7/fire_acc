from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "create_acc")
async def create(query: CallbackQuery):
    pass