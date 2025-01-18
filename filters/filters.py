from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from core import config
from database import db


class IsAdmin(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.from_user.id in config.tg_bot.admin_ids or message.from_user.id in config.tg_bot.admin_ids


class IsNotRegistration(Filter):
    async def __call__(self, message: Message, state: FSMContext, *args, **kwargs):
        state_value = await state.get_state()
        return state_value in [None, default_state]


class IsFundraiser(Filter):
    async def __call__(self, update: Message | CallbackQuery, *args, **kwargs):
        """
        Проверяет, является ли пользователь сборщиком.
        :param update: Сообщение от пользователя.
        :return: True, если пользователь является сборщиком, иначе False.
        """
        # Получение пользователя из базы данных
        fundraiser = await db.get_fundraiser(update.from_user.id)
        return fundraiser is not None
