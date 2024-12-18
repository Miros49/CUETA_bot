from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext

from core import bot
from database import db
from keyboards import UserKeyboards
from lexicon import LEXICON, buttons, callbacks, other
from states import UserState
from utils import validate_and_format_phone_number, convert_string_to_date

router: Router = Router()
kb: UserKeyboards = UserKeyboards()


@router.message(CommandStart())
async def start(message: Message):
    if not await db.user_exists(message.from_user.id):
        await db.init_user(message.from_user.id, message.from_user.username)

    await message.answer(LEXICON['start'], reply_markup=kb.start())


@router.callback_query(F.data == callbacks[buttons['upcoming_events']])
async def start_button_handler(callback: CallbackQuery):
    events: list[dict] = await db.get_all_events()

    if not events:
        return await callback.message.edit_text(LEXICON['no_upcoming_events'])

    await callback.message.edit_text(LEXICON['events_list'], reply_markup=kb.events_list(events))


@router.callback_query(F.data.startswith('event_info'))
async def event_info_handler(callback: CallbackQuery):
    event = await db.get_event(int(callback.data.split('_')[-1]))

    await callback.message.edit_text(
        text=LEXICON['event_info'].format(event.name, event.description, event.date),
        reply_markup=kb.register_to_event(event.id)  # TODO: добавить кнопку "назад"
    )


@router.callback_query(F.data.startswith('register_for_the_event'))
async def register_for_the_event_handler(callback: CallbackQuery, state: FSMContext):
    standard_registration = (callback.data.split('_')[-2] == 'standard')
    user = await db.get_user(callback.from_user.id)
    event_id = int(callback.data.split('_')[-1])
    event = await db.get_event(event_id)

    if not (user.name and user.date_of_birth) and standard_registration:
        message = await callback.message.edit_text(LEXICON['you_need_to_sign_in'])  # TODO: кнопка отмены ведёт в меню

        await state.set_state(UserState.sign_in_enter_name)
        return await state.update_data(registration_message_id=message.message_id, registration_to_event=event_id)

    try:
        await db.create_registration(event.id, user.id)
    except Exception as e:
        print(f"\nОшибка при попытке регистрации пользователя {user.id}\n{e}\n")
        return await callback.message.edit_text(LEXICON['error_occurred'])

    await callback.message.edit_text(
        text=LEXICON['registration_to_event_confirmed'].format(event.name, event.date)
    )  # TODO: добавить кнопку включить уведы если их нет


@router.message(StateFilter(UserState.sign_in_enter_name))
async def sign_in_enter_name_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    name = message.text
    if len(name.split()) != 3:  # TODO: сделать норм систему проверки правильности
        try:
            return await bot.edit_message_text(
                chat_id=message.chat.id, message_id=data['registration_message_id'],
                text='Неверный формат ввода имени. Попробуйте ещё раз'
            )  # TODO: кнопка назад на предыдущий этап
        except TelegramBadRequest:
            pass

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['registration_message_id'],
        text=LEXICON['sign_in_enter_date_of_birth'].format(name.split()[1])
    )  # TODO: кнопку на предыдущий этап

    await state.set_state(UserState.sign_in_enter_date_of_birth)
    await state.update_data(name=name)


@router.message(StateFilter(UserState.sign_in_enter_date_of_birth))
async def sign_in_enter_date_of_birth_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    date_of_birth = message.text
    if not date_of_birth:  # TODO: сюда тоже функцию проверки правильности даты (все подобные выносить в /utils/)
        pass

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['registration_message_id'],
        text=LEXICON['sign_in_enter_status']
    )  # TODO: кнопку на предыдущий этап

    await state.set_state(UserState.sign_in_enter_status)
    await state.update_data(date_of_birth=date_of_birth)


@router.message(StateFilter(UserState.sign_in_enter_status))
async def sign_in_enter_status_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    if message.text not in other['statuses']:
        try:
            return await bot.edit_message_text(
                chat_id=message.chat.id, message_id=data['registration_message_id'],
                text=LEXICON['sign_in_enter_status_again']
            )  # TODO: кнопку на предыдущий этап
        except TelegramBadRequest:
            pass

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['registration_message_id'],
        text=LEXICON['sign_in_enter_phone_number']
    )  # TODO: кнопку на предыдущий этап

    additional_message = await message.answer(
        text=LEXICON['sign_in_enter_phone_number_additional'],
        reply_markup=kb.request_phone_number()
    )

    await state.set_state(UserState.sign_in_enter_phone_number)
    await state.update_data(status=message.text, registration_additional_message_id=additional_message.message_id)


@router.message(StateFilter(UserState.sign_in_enter_phone_number))
async def sign_in_enter_status_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    phone_number = await validate_and_format_phone_number(
        message.contact.phone_number if message.contact else message.text)

    if not phone_number['valid']:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id, message_id=data['registration_message_id'],
                text=LEXICON['sign_in_enter_phone_number_again'].format(phone_number['reason'])
            )  # TODO: кнопка назад на предыдущий этап
        except TelegramBadRequest:
            pass

    await bot.delete_message(message.chat.id, data['registration_additional_message_id'])
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['registration_message_id'],
        text=LEXICON['sign_in_confirmation'].format(
            data['name'], data['date_of_birth'], data['status'], phone_number['formatted']
        ), reply_markup=kb.confirm_registration()
    )

    await state.set_state(UserState.default_state)
    await state.update_data(phone_number=phone_number['formatted'])


@router.callback_query(
    F.data.in_([callbacks[buttons['confirm_registration']], callbacks[buttons['cancel_registration']]])
)
async def confirm_registration_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data.split('_')[-1] == 'canceled':
        return await callback.message.edit_text('Регистрация отменена')

    date_of_birth = await convert_string_to_date(data['date_of_birth'])

    try:
        await db.set_user(
            callback.from_user.id, data['name'], date_of_birth, data['status'], data['phone_number']
        )
    except Exception as e:
        print(f'\nОшибка при попытке добавления информации о пользователе:\n{e}\n')
        return await callback.answer(LEXICON['error_occurred'], show_alert=True)

    await callback.message.edit_text('✅ Информация о вашем аккаунте сохранена!')

    if data['registration_to_event']:
        event = await db.get_event(data['registration_to_event'])
        await callback.message.answer(
            text=LEXICON['event_info'].format(event.name, event.description, event.date),
            reply_markup=kb.register_to_event(event.id)  # TODO: добавить кнопку "назад"
        )


@router.callback_query(F.data == callbacks[buttons['help']])
async def help_button_handler(callback: CallbackQuery):
    await callback.message.answer('Какой-то текст')
