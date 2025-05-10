from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.psql.service import run_sql, CreateAccount

router = Router()
SUPER_USER_ID = 1646823843


@router.message(Command("plat"))
async def plat(message: Message):
    if message.from_user.id != SUPER_USER_ID:
        await message.answer("Sorry? no support?")
        return
    """
    If status is true, request looking /plat receiver_id|true|username|password
    If status is false, request looking /plat receiver_id|false
    """

    _, cmd_options = message.text.split()
    print(cmd_options)
    cmd_options = cmd_options.split("|")
    receiver_id, status = cmd_options[0], cmd_options[1]
    if status.lower() == 'true':
        username, password = cmd_options[2], cmd_options[3]
        await run_sql(CreateAccount(username, password))
        await message.bot.send_message(receiver_id, "Ваш аккаунт одобрен и готов к прогреванию✅ Нажмите /start")
    else:
        await message.bot.send_message(receiver_id,
                                       "Ваш аккаунт не существует или имеет дополнительные системы безнапасности.😞"
                                       " Нажмите /create_account чтобы попробовать снова")
