from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

from database import db


class UserInitialization(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        update: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not await db.user_exists(update.from_user.id):
            await db.init_user(update.from_user.id, update.from_user.username)

        return await handler(update, data)
