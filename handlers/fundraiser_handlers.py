from aiogram import F, Router, exceptions
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from core import bot, config
from database import db
from filters import IsAdmin
from filters.filters import IsFundraiser
from keyboards import AdminKeyboards, UserKeyboards
from lexicon import LEXICON, callbacks, buttons

router: Router = Router()
router.message.filter(IsFundraiser())
router.callback_query.filter(IsFundraiser())


@router.callback_query(F.data.startswith('fundraiser_payment_confirmation'))
async def admin_manu_handler(callback: CallbackQuery, state: FSMContext):
    registration_id = int(callback.data.split('_')[-1])
    registration = await db.get_registration(registration_id)

    await callback.message.edit_reply_markup(reply_markup=None)

    if callback.data.split('_')[-2] == 'confirm':
        await db.update_registration_status(registration_id, 'confirmed')
        await db.move_verification_to_verified(callback.from_user.id)
        await callback.answer(
            f'✅ Регистрация пользователя '
            f'{("@" + registration.username) if registration.username else registration.user_id} сохранена\n'
            f'На всякий сделай скрин',
            show_alert=True
        )

        await bot.send_message(
            chat_id=registration.user_id,
            text='✅ Регистрация на мероприятие подтверждена!'
        )

    else:
        await callback.message.edit_caption(
            caption=(
                f'Пожалуйста, свяжись с этим болваном лично. У меня не было времени это автоматизировать, сори\n'
                f'{("@" + registration.username) if registration.username else registration.user_id} сохранена\n'
            )
        )
        await bot.send_message(
            chat_id=registration.user_id,
            text=f'<b>🤕 Похоже, что-то не так с оплатой.\n'
                 f'Скоро с тобой свяжется наш менеджер: @{callback.from_user.username}</b>'
        )
