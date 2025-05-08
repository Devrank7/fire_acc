from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from utils.security_util import is_admin


class AdminMsgMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        username = event.from_user.username or f"user{event.from_user.id}"
        print("Username", username)
        if not is_admin(username):
            await event.answer("Извините, вход вам запрещен!")
            return
        return await handler(event, data)


class AdminCallbackMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        username = event.from_user.username or f"user{event.from_user.id}"
        print("Username", username)
        if not is_admin(username):
            await event.answer("Извините, вход вам запрещен!", show_alert=True)
            return
        return await handler(event, data)
