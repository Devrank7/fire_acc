import datetime
from datetime import timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from db.psql.service import run_sql, ReadAllAccounts, ReadAccountByID
from keyboards.keyboards import ListKeyboardMarkup
from middleware import AdminMsgMiddleware, AdminCallbackMiddleware

router = Router()
router.message.middleware(AdminMsgMiddleware())
router.message.middleware(AdminCallbackMiddleware())

@router.message(Command("my_accounts"))
async def me_cmd(message: Message, state: FSMContext):
    accounts = await run_sql(ReadAllAccounts())
    if len(accounts) == 0:
        await message.answer("Вы пока что не добавили ни одного фейсбук аккаунта для прогрева. Нажмите /create_account")
        return
    account_markup_exe = ListKeyboardMarkup(accounts, lambda acc: acc.username, lambda acc: acc.id, "acc_", False, 0)
    markup = account_markup_exe.as_keyboard_markup()
    text = 'Выберете аккаунт: '
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await message.answer("Выберете аккаунт: ", reply_markup=markup)


@router.callback_query(F.data == "my_acc")
async def my(query: CallbackQuery, state: FSMContext):
    accounts = await run_sql(ReadAllAccounts())
    if len(accounts) == 0:
        await query.answer("Вы пока что не добавили ни одного фейсбук аккаунта для прогрева. Нажмите /create_account", show_alert=True)
        return
    account_markup_exe = ListKeyboardMarkup(accounts, lambda acc: acc.username, lambda acc: acc.id, "acc_", True, 0)
    markup = account_markup_exe.as_keyboard_markup()
    text = 'Выберете аккаунт: '
    await state.update_data(bt1=text)
    await state.update_data(br1=markup)
    await query.message.edit_text("Выберете аккаунт: ", reply_markup=markup)

@router.callback_query(F.data.startswith("acc_"))
async def acc(query: CallbackQuery, state: FSMContext):
    acc_id = int(query.data.split("_")[1])
    account = await run_sql(ReadAccountByID(acc_id))
    if not account:
        await query.answer("Такого аккаунта не существует ❌", show_alert=True)
        return
    fire_end: datetime = account.fire_end
    now = datetime.datetime.now()
    days_for_fire = fire_end - now
    firing_days = now - account.created_at
    is_fire = days_for_fire < timedelta(0)

    # Функция форматирования timedelta в "X дней Y часов"
    def format_timedelta(td: timedelta) -> str:
        total_seconds = int(td.total_seconds())
        abs_total_seconds = abs(total_seconds)
        days = abs_total_seconds // 86400
        hours = (abs_total_seconds % 86400) // 3600
        return f"{'-' if total_seconds < 0 else ''}{days} дн. {hours} ч."

    text = f'''
    Аккаунт:
    Почта/номер: {account.username},
    Пароль: {account.password},
    Прогрев: {"Завершён ✅" if is_fire else f"Идёт ({format_timedelta(firing_days)})"},
    Осталось до конца прогрева: {"Готов 🔥" if is_fire else f"\n{format_timedelta(days_for_fire)}"}
    Статус: {"Прогретый ✅" if is_fire else "Прогревается 📋"}
    '''
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data=f"rem_{account.id}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"back_1")]
    ])
    await state.update_data(bt2=text)
    await state.update_data(br2=markup)
    await query.message.edit_text(text, reply_markup=markup)

