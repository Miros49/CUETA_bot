from aiogram import F, Router, exceptions
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from core import bot, config
from database import db
from filters import IsAdmin
from keyboards import AdminKeyboards, UserKeyboards
from lexicon import LEXICON, callbacks, buttons

router: Router = Router()


@router.message(Command('pass'))
async def admin_manu_handler(message: Message, state: FSMContext):
    pass
