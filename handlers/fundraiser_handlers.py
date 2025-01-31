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
async def fundraiser_payment_confirmation_handler(callback: CallbackQuery):
    registration_id = int(callback.data.split('_')[-1])
    registration = await db.get_registration_by_id(registration_id)

    await callback.message.edit_reply_markup(reply_markup=None)

    if callback.data.split('_')[-2] == 'confirm':
        await db.update_registration_status(registration_id, 'confirmed')
        await db.move_verification_to_verified(callback.from_user.id)

        await callback.answer(
            f'✅ Регистрация пользователя '
            f'{("@" + registration.username) if registration.username else registration.user_id} сохранена\n',
            show_alert=True
        )

        await bot.send_message(
            chat_id=registration.user_id,
            text='✅ Оплата регистрации на мероприятие подтверждена!'
        )

    else:
        await db.update_registration_status(registration_id, 'personal')
        await callback.message.edit_caption(
            caption=(
                f'Пожалуйста, свяжись с этим болваном лично. У меня не было времени это автоматизировать, сори\n'
                f'{("@" + registration.username) if registration.username else registration.user_id}\n'
            )
        )
        await bot.send_message(
            chat_id=registration.user_id,
            text=f'<b>🤕 Похоже, что-то не так с оплатой.\n'
                 f'Скоро с тобой свяжется наш менеджер: @{callback.from_user.username}</b>'
        )


@router.callback_query(F.data.startswith('fundraiser_transaction_confirmation'))
async def fundraiser_transaction_confirmation_handler(callback: CallbackQuery):
    transaction_id = int(callback.data.split('_')[-1])
    transaction = await db.get_transaction_by_id(transaction_id)
    user = await db.get_user(transaction.user_id)

    if callback.data.split('_')[-2] == 'confirm':
        await db.update_user_balance(user.id, transaction.coins_amount)
        await db.update_transaction_status(transaction_id, 'confirmed')
        await db.move_left_to_confirm_to_confirmed(callback.from_user.id)

        await callback.message.edit_caption(
            caption=f'✅ Покупка {transaction.coins_amount} CUETA Coins на сумму {transaction.amount} '
            f'пользователя {("@" + user.username) if user.username else user.user_id} подтверждена',
            reply_markup=None
        )

        await bot.send_message(
            chat_id=transaction.user_id,
            text=f'✅ Покупка {transaction.coins_amount} CUETA Coins подтверждена',
        )

    else:
        await db.update_transaction_status(transaction_id, 'personal')
        await callback.message.edit_caption(
            caption=(
                f'Пожалуйста, свяжись с этим болваном лично. У меня не было времени это автоматизировать, сори\n'
                f'{("@" + user.username) if user.username else user.user_id}\n'
            ), reply_markup=None
        )

        try:
            await bot.send_message(
                chat_id=user.id,
                text=f'<b>🤕 Похоже, что-то не так с оплатой.\n'
                     f'Скоро с тобой свяжется наш менеджер: @{callback.from_user.username}</b>'
            )
        except Exception as e:
            print(f'error id 4: {e}')
