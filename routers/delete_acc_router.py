from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from db.psql.service import run_sql, DeleteAccount
from middleware import AdminCallbackMiddleware

router = Router()
router.message.middleware(AdminCallbackMiddleware())

@router.callback_query(F.data.startswith("rem_"))
async def rem_acc(query: CallbackQuery):
    acc_id = int(query.data.split("_")[1])
    are_you_sure_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data=f"del_{acc_id}")],
            [InlineKeyboardButton(text="Нет", callback_data="back_2")],
        ]
    )
    await query.message.edit_text("Вы уверены ⁉️ \n"
                                  " Если вы удалите аккаунт из бота,"
                                  " то бот больше не сможет его прогревать и уведомлять вас о прогреве❗",
                                  reply_markup=are_you_sure_keyboard)


@router.callback_query(F.data.startswith("del_"))
async def del_acc(query: CallbackQuery):
    acc_id = int(query.data.split("_")[1])
    await run_sql(DeleteAccount(acc_id))
    await query.message.edit_text("Аккаунт был полностью удален✅ Нажмите /start")
