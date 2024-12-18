import asyncio

from aiogram import F, Router, exceptions
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from core import bot
from database import db
from filters import IsAdmin
from keyboards import AdminKeyboards, UserKeyboards
from lexicon import LEXICON, callbacks, buttons
from states import AdminState
from utils import convert_string_to_date


router: Router = Router()
kb: AdminKeyboards = AdminKeyboards()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command('admin'))
async def admin_manu_handler(message: Message, state: FSMContext):
    await message.answer(LEXICON['admin_menu'].format(message.from_user.first_name), reply_markup=kb.menu())

    await state.set_state(AdminState.default_state)


@router.callback_query(F.data == callbacks[buttons['admin_back_to_menu']])
async def admin_menu_callback_handler(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON['admin_menu'], reply_markup=kb.menu())


@router.callback_query(F.data == callbacks[buttons['admin_mailing']])
async def mailing_handler(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON['dev'].format(callback.from_user.first_name), reply_markup=kb.menu())


@router.callback_query(F.data == callbacks[buttons['admin_events']])
async def events_handler(callback: CallbackQuery):
    events = await db.get_all_events()

    await callback.message.edit_text(LEXICON['events_list'], reply_markup=kb.upcoming_events(events))


@router.callback_query(F.data == callbacks[buttons['admin_create_event']])
async def admin_create_event_callback_handler(callback: CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text(LEXICON['admin_add_event_name'])

    await state.set_state(AdminState.enter_event_name)
    await state.update_data(event_creation_message_id=message.message_id)


@router.message(StateFilter(AdminState.enter_event_name))
async def event_name_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['event_creation_message_id'],
        text=LEXICON['admin_add_event_description'].format(message.text)
    )

    await state.set_state(AdminState.enter_event_description)
    await state.update_data(event_name=message.text)


@router.message(StateFilter(AdminState.enter_event_description))
async def event_description_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['event_creation_message_id'],
        text=LEXICON['admin_add_event_date'].format(data['event_name'], message.text)
    )

    await state.set_state(AdminState.enter_event_date)
    await state.update_data(event_description=message.text)


@router.message(StateFilter(AdminState.enter_event_date))
async def event_date_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()  # TODO: нужно проверять дату на правильность ввода + добавить везде кнопки "назад"

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['event_creation_message_id'],
        text=LEXICON['admin_create_event'].format(
            data['event_name'], data['event_description'], message.text
        ), reply_markup=kb.confirm_creation_of_event()
    )

    await state.update_data(event_date=message.text)
    await state.set_state(AdminState.default_state)


@router.callback_query(F.data.in_(
    [callbacks[buttons['admin_creation_of_event_confirm']], callbacks[buttons['admin_creation_of_event_cancel']]])
)
async def create_event_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data.split('_')[-1] == 'confirm':
        try:
            event_date = await convert_string_to_date(data['event_date'])

            event_id = await db.create_event(data['event_name'], data['event_description'], event_date)

        except Exception as e:
            print(f'Ошибка при попытке создания мероприятия: {e}')

            return await callback.message.answer(LEXICON['error_occurred'])

        await callback.message.edit_text(
            text=LEXICON['admin_event_created'].format(
                data['event_name'], data['event_description'], data['event_date']
            ),  # TODO: написать функцию, которая будет вытаскивать значения из сообщения
            # TODO: сюда же кнопку удаления мероприятия
        )

<<<<<<< HEAD
        for user in await db.get_all_users():
            try:
                await bot.send_message(
                    chat_id=user.id,
                    text=LEXICON['new_event_notification'].format(
                        data['event_name'], data['event_description'], data['event_date']
                    ),
                    reply_markup=UserKeyboards.register_to_event(event_id)
                )
                await asyncio.sleep(0.07)  # задержка чтоб не заблокировали

            except TelegramBadRequest:
                pass
=======
        # for user in await db.get_all_users():
        #     try:
        #         await bot.send_message(
        #             chat_id=user.id,
        #             text=LEXICON['new_event_notification'].format(
        #                 data['event_name'], data['event_description'], data['event_date']
        #             ),
        #             reply_markup=UserKeyboards.register_to_event(event_id)
        #         )
        #         await asyncio.sleep(0.07)  # задержка чтоб не заблокировали

        #     except TelegramBadRequest:
        #         pass
>>>>>>> 9ec116f (prod_bugfixes_3)

    await callback.message.edit_text(LEXICON['admin_event_creation_canceled'], reply_markup=kb.back_to_menu())


def todo() -> None:
    # TODO: вместо кнопки помощь "по вопросам пишите туда"
    return None
