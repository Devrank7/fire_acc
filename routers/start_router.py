from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from middleware import AdminMsgMiddleware

router = Router()
router.message.middleware(AdminMsgMiddleware())
start_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать аккаунт", callback_data="create_acc")],
    [InlineKeyboardButton(text="Мои аккаунты", callback_data="my_acc")],
])
text = '''
Привет! 👋
Это бот создан для автоматизации прогрева ваших фейсбук аккаунтов.
Бот позволяет прогреть ваши фейсбук аккаунты за 21 день
и следить за тем сколько осталось до полного прогревания и уведомлять вас по завершению этого процесса.
В боте присутствует такие команды 💬:
- /start - команда для запуска бота
- /my_accounts - мои аккаунты для прогревания и управления ними
- /create_account - создать аккаунт для прогрева
Примечания 🪶:
- Что бы вернутся в главное меню введите /start (может быть полезно если вы где то застряли в боте)
- Одновременно можно прогревать только 5 фейсбук аккаунтов!
'''

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await state.update_data(bt0=text)
    await state.update_data(br0=start_button)
    await message.answer(text, reply_markup=start_button)
