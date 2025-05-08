from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data.startswith('back_'))
async def back(query: CallbackQuery, state: FSMContext):
    await query.answer()
    index = query.data.split("_")[1]
    data = await state.get_data()
    text_data = data.get(f"bt{index}")
    reply_data = data.get(f"br{index}")
    await query.message.edit_text(text_data, reply_markup=reply_data)