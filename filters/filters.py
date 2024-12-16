from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from core import config
from database import db


class IsAdmin(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.from_user.id in config.tg_bot.admin_ids or message.from_user.id in config.tg_bot.admin_ids
