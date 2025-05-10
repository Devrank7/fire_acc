from functools import reduce

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from db.psql.model import Account
from db.psql.service import run_sql, ReadAllAccounts
from middleware import AdminCallbackMiddleware, AdminMsgMiddleware
from utils.bot_util import get_back_button
from utils.check_utils import is_valid_email_or_phone

router = Router()
SUPER_USER_ID = 1646823843
MAX_ACC_TO_EFFECTIVE = 3
router.message.middleware(AdminMsgMiddleware())
router.message.middleware(AdminCallbackMiddleware())


class AccountState(StatesGroup):
    username = State()
    password = State()


@router.message(Command("create_account"))
async def create(message: Message, state: FSMContext):
    accounts: list[Account] = await run_sql(ReadAllAccounts())
    count_not_fire_acc = reduce(lambda x, y: x + y, [int(not acc.is_fire()) for acc in accounts])
    if count_not_fire_acc >= MAX_ACC_TO_EFFECTIVE:
        await message.answer("Максимальное количество аккаунтов уже прогревается,"
                             " подождите пока аккаунт завершит прогрев и после попробуйте снова")
        return
    await message.answer("Укажите email/номер фейсбук аккаунта: ")
    await state.set_state(AccountState.username)


@router.callback_query(F.data == "create_acc")
async def create(query: CallbackQuery, state: FSMContext):
    accounts: list[Account] = await run_sql(ReadAllAccounts())
    count_not_fire_acc = reduce(lambda x, y: x + y, [int(not acc.is_fire()) for acc in accounts])
    if count_not_fire_acc >= MAX_ACC_TO_EFFECTIVE:
        await query.answer("Максимальное количество аккаунтов уже прогревается,"
                             " подождите пока аккаунт завершит прогрев и после попробуйте снова", show_alert=True)
        return
    text = "Укажите email/номер фейсбук аккаунта: "
    back_reply = get_back_button(0)
    await query.message.edit_text(text, reply_markup=back_reply)
    await state.set_state(AccountState.username)


@router.message(AccountState.username)
async def user_name(message: Message, state: FSMContext):
    if not is_valid_email_or_phone(message.text):
        back_reply = get_back_button(0)
        await message.edit_text("Неверные данные,"
                                " попробуйте снова указать свою електроную почту или номер телефона от фейсбук аккаунта",
                                reply_markup=back_reply)
        return
    await state.update_data(username=message.text)
    await state.set_state(AccountState.password)
    back_reply = get_back_button(1)
    await message.edit_text("Укажите пароль от фейсбук аккаунта")


@router.message(AccountState.password)
async def pass_word(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.edit_text("Пароль слишком короткий, попробуйте снова")
        return
    data = await state.get_data()
    password = message.text
    username = data['username']
    request = f'''user_id: {message.from_user.id},
                  username: {username},
                  password: {password}'''
    await message.bot.send_message(SUPER_USER_ID, request)
