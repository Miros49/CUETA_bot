import asyncio
from datetime import date, datetime, timedelta

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.fsm.context import FSMContext

from core import bot, BEER_PONG_EVENT_ID
from database import db
from filters import IsNotRegistration
from keyboards import UserKeyboards, FundraiserKeyboards
from lexicon import LEXICON, buttons, callbacks, status_callback_to_string
from states import UserState
from utils import validate_and_format_phone_number, convert_string_to_date, validate_date_of_birth, get_user_state
from utils.utils import is_user_adult

router: Router = Router()
kb: UserKeyboards = UserKeyboards()
fundraiser_kb: FundraiserKeyboards = FundraiserKeyboards()
key = True

@router.message(Command('/clear_08264875'))
async def cls(message: Message, state: FSMContext):
    await message.delete()

    if key:
        mes = await message.answer('Привет, Антон!')
        mes2 = await message.answer('Состояние сброшено')

        await asyncio.sleep(2)
        await mes.delete()

        await asyncio.sleep(1)
        await mes2.delete()

        await state.set_state(UserState.default_state)
        key = False
        print('anton')

    else:
        mes = await message.answer('Не хитри')
        print('anton canceled')

        await asyncio.sleep(2)
        await mes.delete()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(UserState.default_state)

    if not await db.user_exists(message.from_user.id):
        await db.init_user(message.from_user.id, message.from_user.username)

    await message.answer(LEXICON['start'], reply_markup=kb.start())

    command_text = message.text.split(' ', 1)[1:]
    if command_text:
        # if command_text[-1].startswith('beer_pong_invite'):
        #     player_1_id = int(command_text[-1].split('_')[-1])
        #
        #     if player_1_id == message.from_user.id:
        #         return await message.answer(LEXICON['ref_error'])
        #     elif await db.is_user_in_team(message.from_user.id):
        #         return await message.answer(LEXICON['ref_abuse'])
        #
        #     try:
        #         player_1 = await db.get_user(player_1_id)
        #         team_id = await db.create_team(player_1_id, player_1.username, message.from_user.id,
        #                                        message.from_user.username)
        #
        #         await message.answer(LEXICON['beer_pong_team_registered'].format(player_1.username, team_id))
        #         await bot.send_message(
        #             chat_id=player_1_id,
        #             text=LEXICON['beer_pong_team_registered'].format(message.from_user.username, team_id)
        #         )
        #
        #         await db.create_registration(BEER_PONG_EVENT_ID, player_1_id)
        #         await db.create_registration(BEER_PONG_EVENT_ID, message.from_user.id)
        #
        #     except Exception as e:
        #         print(f"\nОшибка при попыткесоздания команды на бирпонг:\n{e}\n")
        #         return await message.answer(LEXICON['beer_pong_registration_team_errored'])
        pass


@router.message(Command('menu'))
async def menu_command_handler(message: Message):
    pass


@router.callback_query(F.data == callbacks[buttons['help']], IsNotRegistration())
async def help_button_handler(callback: CallbackQuery):
    await callback.message.answer(LEXICON['help'])


@router.message(F.text == buttons['upcoming_events'], IsNotRegistration())
async def start_button_handler(message: Message):
    events: list[dict] = await db.get_upcoming_events()

    if not events:
        return await message.answer(LEXICON['no_upcoming_events'])

    await message.answer(LEXICON['events_list'], reply_markup=kb.events_list(events))


@router.callback_query(F.data == callbacks[buttons['upcoming_events']], IsNotRegistration())
async def start_button_handler(callback: CallbackQuery):
    events: list[dict] = await db.get_upcoming_events()

    if not events:
        return await callback.message.edit_text(LEXICON['no_upcoming_events'])

    if callback.message.photo:
        await callback.message.delete()
        return await callback.message.answer(LEXICON['events_list'], reply_markup=kb.events_list(events))

    await callback.message.edit_text(LEXICON['events_list'], reply_markup=kb.events_list(events))


@router.callback_query(F.data.startswith('event_info'))
async def event_info_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    event = await db.get_event(int(callback.data.split('_')[-1]))
    registration = await db.get_registration(event.id, callback.from_user.id)

    registration_text, kb_arg, kb_additional_arg, show_instruction = '', True, False, False
    if registration:
        kb_arg = False
        kb_additional_arg = True

        if registration.registration_type == 'pre-registration':
            registration_text = LEXICON['pre-registration_to_event_confirmed']
        else:
            registration_text = '\n\n✅ Вы уже зарегистрированы на это мероприятие'

        if registration.status == 'confirmed':
            kb_additional_arg = False

    try:
        await callback.message.delete()
    except Exception as e:
        print('error id: 1', e)
    
    await callback.message.answer_photo(
        photo=event.photo_id,
        caption=LEXICON['event_info'].format(event.description, registration_text),
        reply_markup=kb.register_to_event(event.id, kb_arg, kb_additional_arg)
    )


@router.callback_query(F.data.startswith('cancel_registration_beer_pong'))
async def cancel_registration_beer_pong_handler(callback: CallbackQuery):
    if callback.data.split('_')[-1] == 'visitor':
        if await db.remove_registration(BEER_PONG_EVENT_ID, callback.from_user.id):
            await callback.message.delete()
            return await callback.message.answer(
                '<b>✅ Регистрация на мероприятие снята</b>',
                reply_markup=kb.start()
            )
        else:
            return await callback.message.edit_text(
                'Произошла ошибка: вашей регистрации не существует.\nПожалуйста, обратитесь к @Miros49')
    else:
        return await callback.message.edit_text(
            '<b>Пожалуйста, свяжитесь с @ShIN_66</b>'
        )


@router.callback_query(F.data.startswith('register_for_the_event'), IsNotRegistration())
async def register_for_the_event_handler(callback: CallbackQuery, state: FSMContext):
    registration_type = callback.data.split('_')[-2]
    user = await db.get_user(callback.from_user.id)
    event_id = int(callback.data.split('_')[-1])
    event = await db.get_event(event_id)
    registration = await db.get_registration(event.id, callback.from_user.id)

    if not (user.name and user.date_of_birth):
        try:
            await callback.message.delete()
        except Exception as e:
            print('error id 2', e)
        message = await callback.message.answer(
            text=LEXICON['you_need_to_sign_in'],
            reply_markup=kb.cancel_registration()
        )

        await state.set_state(UserState.sign_in_enter_name)
        return await state.update_data(registration_message_id=message.message_id, registration_to_event=event_id)

    if registration:
        await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id,
            reply_markup=None
        )
        return await callback.answer('✅ Вы уже зарегистрированы на данное мероприятие', show_alert=True)

    if 0:
        additional_text = LEXICON['pre-registration_to_event_confirmed']
        send_instructions = False
    else:
        additional_text = LEXICON['see_payment_instructions_below']
        send_instructions = True

    try:
        await callback.message.edit_caption(
            caption=LEXICON['event_info'].format(event.description, additional_text),
        )
    except Exception as e:
        print(f'Ошибка при попытке изменения подписи (register_for_the_event_handler): {e}')

    if send_instructions:
        try:
            fundraiser = await db.get_fundraiser_with_least_registrations()

            try:
                await db.create_registration(
                    event.id, user.id, user.username, 0,
                    registration_type, fundraiser.id, 'processing'
                )
            except Exception as e:
                print(f"\nОшибка при попытке регистрации пользователя {user.id}\n{e}\n")
                await callback.message.delete()
                return await callback.message.answer(LEXICON['error_occurred'])

            registration = await db.get_registration(event.id, callback.from_user.id)
            await db.assign_fundraiser_to_registration(registration.id, fundraiser.id)
            await db.increment_registration_count(fundraiser.id)
            await db.update_registration_status(registration.id, 'waiting_for_payment')

            print(
                f'FUNDRAISER {fundraiser.username} assigned for registration {registration.id} '
                f'({("@" + registration.username) if registration.username else registration.user_id})\n'
                f'{(datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")}\n'
            )

            await db.set_first_warning(registration.id)

            if is_user_adult(user.date_of_birth):
                text = LEXICON['payment_instructions'].format(
                    '', 1, fundraiser.phone_number, fundraiser.preferred_bank, 2, fundraiser.username
                )
            else:
                text = LEXICON['payment_instructions'].format(
                    LEXICON['underage_instruction'].format(fundraiser.username), 2, fundraiser.phone_number,
                    fundraiser.preferred_bank, 3, fundraiser.username
                )

            await callback.message.answer(
                text=text,
                reply_markup=kb.confirm_payment(event.id)
            )

        except Exception as e:
            await callback.message.answer(LEXICON['error_occurred'])
            print(f'Ошибка при попытке отправки инструкции: {e}')


@router.callback_query(F.data.startswith('send_payment_confirmation'))
async def send_payment_confirmation(callback: CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split('_')[-1])
    user = await db.get_user(callback.from_user.id)
    registration = await db.get_registration(event_id, callback.from_user.id)

    await callback.message.edit_reply_markup(reply_markup=None)

    if not (user.name and user.date_of_birth):
        try:
            pre_registration_message = await callback.message.answer(
                text=LEXICON['seems_like_your_profile_unfilled']
            )

            state = get_user_state(user.id)
            await state.set_state(UserState.sign_in_enter_name)
            return await state.update_data(
                registration_message_id=pre_registration_message.message_id, pre_registration_filling_profile=True
            )

        except Exception as e:
            return print(f'ошибка при попытке заставить дауна заполнить профиль: {e}')

    if registration.status != 'waiting_for_payment':
        print(
            f'\n\nтипок не может скинуть подтверждение оплаты. '
            f'статус регистрации: {registration.status}, пользователь: {callback.from_user.id}'
        )
        await state.set_state(UserState.default_state)
        return await callback.answer(
            'Что-то пошло не так. Пожалуйста, свяжись с назначенным тебе менеджером, если оплата всё ещё не завершена')

    last_payment_confirmation_message_message_id = (
        await callback.message.answer(
            text=LEXICON['payment_confirmation_text'],
            reply_markup=kb.cancel_payment_confirmation(event_id)
        )
    ).message_id

    await db.update_registration_status(registration.id, 'ready_to_confirm_payment')

    await state.set_state(UserState.send_payment_confirmation)
    await state.update_data(event_id=event_id, registration_id=registration.id,  # TODO: нужно добавлять это раньше
                            last_payment_confirmation_message_message_id=last_payment_confirmation_message_message_id)


@router.message(StateFilter(UserState.send_payment_confirmation))
async def send_payment_confirmation_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    event_id, registration_id = data['event_id'], data['registration_id']
    registration = await db.get_registration_by_id(registration_id)
    user = await db.get_user(message.from_user.id)

    if not registration.fundraiser_id:
        print("для мироса (всё норм, это не ошибка)")
        fundraiser = await db.get_fundraiser_with_least_registrations()
        await db.assign_fundraiser_to_registration(registration.id, fundraiser.id)
        await db.increment_registration_count(fundraiser.id)

        print(
            f'FUNDRAISER {fundraiser.username} assigned for registration {registration.id} '
            f'({("@" + registration.username) if registration.username else registration.user_id})\n'
            f'{(datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")}\n'
        )

    try:
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id, message_id=data['last_payment_confirmation_message_message_id'],
            reply_markup=None
        )
    except Exception as e:
        print(f'фигня с удалением клавиатурыы отмены поддтверждения: {e}')

    if not (message.photo or message.document):
        last_payment_confirmation_message_message_id = (
            await message.answer(
                text=LEXICON['payment_confirmation_text_again'],
                reply_markup=kb.cancel_payment_confirmation(event_id)
            )
        ).message_id
        return await state.update_data(
            last_payment_confirmation_message_message_id=last_payment_confirmation_message_message_id
        )

    underage_text = '' if is_user_adult(user.date_of_birth) \
        else '\n‼️ Необходимо проверить согласие от родителей'
    caption = (
        f'<b>Оплата от {("@" + registration.username) if registration.username else registration.user_id}'
        f'{underage_text}</b>'
    )

    if message.photo:
        await bot.send_photo(
            chat_id=registration.fundraiser_id, photo=message.photo[-1].file_id,
            caption=caption,
            reply_markup=fundraiser_kb.confirm_payment(registration_id)
        )
    else:
        await bot.send_document(
            chat_id=registration.fundraiser_id, document=message.document.file_id,
            caption=caption,
            reply_markup=fundraiser_kb.confirm_payment(registration_id)
        )

    await message.answer('<b>Круто! 🔥\nОсталось только дождаться подтверждения оплаты. Скоро свяжемся с тобой 😉</b>')

    await db.decrement_registration_and_increment_verification(registration.fundraiser_id)
    await db.update_registration_status(registration_id, 'waiting_for_fundraiser_confirmation')

    await state.set_state(UserState.default_state)


@router.message(StateFilter(UserState.sign_in_enter_name))
async def sign_in_enter_name_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    name = message.text.strip()

    await message.delete()

    if len(name.split()) != 3:
        try:
            return await bot.edit_message_text(
                chat_id=message.chat.id, message_id=data['registration_message_id'],
                text=LEXICON['sign_in_enter_name_again'],  # TODO: кнопку, если нет отчества
                reply_markup=kb.cancel_registration()
            )
        except TelegramBadRequest:
            return

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['registration_message_id'],
        text=LEXICON['sign_in_enter_date_of_birth'].format(name.split()[1]),
        reply_markup=kb.profile_registration_back_to_name()
    )

    await state.set_state(UserState.sign_in_enter_date_of_birth)
    await state.update_data(name=name)


@router.message(StateFilter(UserState.sign_in_enter_date_of_birth))
async def sign_in_enter_date_of_birth_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    date_of_birth = message.text
    validation_check = validate_date_of_birth(date_of_birth)

    if not validation_check['valid']:
        try:
            return await bot.edit_message_text(
                chat_id=message.chat.id, message_id=data['registration_message_id'],
                text=LEXICON['sign_in_enter_date_of_birth_again'].format(validation_check['reason']),
                reply_markup=kb.profile_registration_back_to_name()
            )
        except TelegramBadRequest:
            return

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['registration_message_id'],
        text=LEXICON['sign_in_enter_status'],
        reply_markup=kb.enter_status()
    )

    await state.set_state(UserState.sign_in_enter_status)
    await state.update_data(date_of_birth=date_of_birth)


@router.callback_query(
    F.data.in_([
        callbacks[buttons['registration_status_bachelor-cu']], callbacks[buttons['registration_status_master-cu']],
        callbacks[buttons['registration_status_other']], callbacks[buttons['registration_status_t-bank']]]),
    StateFilter(UserState.sign_in_enter_status)
)
async def sign_in_enter_status_handler(callback: CallbackQuery, state: FSMContext):
    status = status_callback_to_string.get(callback.data, 'unknown')

    await callback.message.edit_text(
        text=LEXICON['sign_in_enter_phone_number'],
        reply_markup=kb.profile_registration_back_to_status()
    )

    additional_message = await callback.message.answer(
        text=LEXICON['sign_in_enter_phone_number_additional'],
        reply_markup=kb.request_phone_number()
    )

    await state.set_state(UserState.sign_in_enter_phone_number)
    await state.update_data(status=status, registration_additional_message_id=additional_message.message_id)


@router.message(StateFilter(UserState.sign_in_enter_phone_number))
async def sign_in_enter_status_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    phone_number = await validate_and_format_phone_number(
        message.contact.phone_number if message.contact else message.text)

    if not phone_number['valid']:
        try:
            return await bot.edit_message_text(
                chat_id=message.chat.id, message_id=data['registration_message_id'],
                text=LEXICON['sign_in_enter_phone_number_again'].format(phone_number['reason']),
                reply_markup=kb.profile_registration_back_to_status()
            )
        except TelegramBadRequest:
            return

    await bot.delete_message(message.chat.id, data['registration_additional_message_id'])
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=data['registration_message_id'],
        text=LEXICON['sign_in_confirmation'].format(
            data['name'], data['date_of_birth'], data['status'], phone_number['formatted']
        ), reply_markup=kb.confirm_registration()
    )

    await state.set_state(UserState.default_state)
    await state.update_data(phone_number=phone_number['formatted'])


@router.callback_query(F.data.startswith('profile_registration_back_to'))
async def profile_registration_back_to_callback(callback: CallbackQuery, state: FSMContext):
    state_value = await state.get_state()
    data = await state.get_data()

    destination = callback.data.split('_')[-1]

    if state_value not in (
            UserState.sign_in_enter_name, UserState.sign_in_enter_date_of_birth,
            UserState.sign_in_enter_status, UserState.sign_in_enter_phone_number
    ) or (state_value in (UserState.default_state, None) and destination != 'phone-number'):
        print(destination, state_value)
        await callback.answer('Для этого перейдите в профиль')
        return await bot.edit_message_reply_markup(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None
        )

    if destination == 'name':
        await callback.message.edit_text(
            text=LEXICON['sign_in_enter_name'],
            reply_markup=kb.cancel_registration() if not data.get('registration_to_event', None) else None
        )
        await state.set_state(UserState.sign_in_enter_name)

    elif destination == 'date-of-birth':
        await callback.message.edit_text(
            text=LEXICON['sign_in_enter_date_of_birth'].format(data['name'].split('_')[1]),
            reply_markup=kb.profile_registration_back_to_name()
        )
        await state.set_state(UserState.sign_in_enter_date_of_birth)

    elif destination == 'status':
        await callback.message.edit_text(
            text=LEXICON['sign_in_enter_status'],
            reply_markup=kb.enter_status()
        )
        await bot.delete_message(chat_id=callback.message.chat.id,
                                 message_id=data['registration_additional_message_id'])
        await state.set_state(UserState.sign_in_enter_status)

    else:
        await callback.message.edit_text(
            text=LEXICON['sign_in_enter_phone_number'],
            reply_markup=kb.profile_registration_back_to_status()
        )
        await callback.message.answer(
            text=LEXICON['sign_in_enter_phone_number_additional'],
            reply_markup=kb.request_phone_number()
        )
        await state.set_state(UserState.sign_in_enter_phone_number)


@router.callback_query(
    F.data.in_([callbacks[buttons['confirm_registration']], callbacks[buttons['cancel_registration']]])
)
async def confirm_registration_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data.split('_')[-1] == 'canceled':
        await callback.message.edit_text('<b>✅ Регистрация отменена</b>')
        return await state.set_state(UserState.default_state)

    date_of_birth = await convert_string_to_date(data['date_of_birth'])

    try:
        await db.set_user(
            callback.from_user.id, data['name'], date_of_birth, data['status'], data['phone_number']
        )
    except Exception as e:
        print(f'\nОшибка при попытке добавления информации о пользователе:\n{e}\n')
        return await callback.answer(LEXICON['error_occurred'], show_alert=True)

    await callback.message.edit_text('✅ Информация о вашем аккаунте сохранена!')

    if data.get('pre_registration_filling_profile', None):
        await callback.message.edit_text(
            text=LEXICON['pre-registration_profile_filled']
        )

        user = await db.get_user(callback.from_user.id)

        try:
            event = await db.get_event(2)
            fundraiser = await db.get_fundraiser_with_least_registrations()
            registration = await db.get_registration(event.id, callback.from_user.id)
            await db.assign_fundraiser_to_registration(registration.id, fundraiser.id)
            await db.increment_registration_count(fundraiser.id)
            await db.update_registration_status(registration.id, 'waiting_for_payment')

            print(
                f'FUNDRAISER {fundraiser.username} assigned for registration {registration.id} '
                f'({("@" + registration.username) if registration.username else registration.user_id})\n'
                f'{(datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")}\n'
            )

            await db.set_first_warning(registration.id)

            if is_user_adult(user.date_of_birth):
                text = LEXICON['payment_instructions'].format(
                    '', 1, fundraiser.phone_number, fundraiser.preferred_bank, 2, fundraiser.username
                )
            else:
                text = LEXICON['payment_instructions'].format(
                    LEXICON['underage_instruction'].format(fundraiser.username), 2, fundraiser.phone_number,
                    fundraiser.preferred_bank, 3, fundraiser.username
                )

            await callback.message.answer(
                text=text,
                reply_markup=kb.confirm_payment(event.id)
            )

        except Exception as e:
            await callback.message.answer(LEXICON['error_occurred'])
            print(f'Ошибка при попытке отправки инструкции: {e}')

        data.pop('pre_registration_filling_profile', None)
        data.pop('registration_message_id', None)
        await state.update_data(**data)

    elif data.get('show_profile', None):
        await profile_callback_handler(callback, state)

        data.pop('show_profile', None)
        await state.update_data(**data)

    elif data.get('registration_to_event', None):
        event = await db.get_event(data['registration_to_event'])
        await callback.message.answer_photo(
            photo=event.photo_id,
            caption=LEXICON['event_info'].format(event.description, ''),
            reply_markup=kb.register_to_event(event.id, True)
        )

        data.pop('registration_to_event', None)
        await state.update_data(**data)


@router.callback_query(F.data == callbacks[buttons['profile']], IsNotRegistration())
async def profile_callback_handler(callback: CallbackQuery, state: FSMContext):
    user = await db.get_user(callback.from_user.id)

    if not (user.name and user.date_of_birth):
        callback = await callback.message.edit_text(LEXICON['you_need_to_sign_in'])  # TODO: кнопка отмены ведёт в меню

        await state.set_state(UserState.sign_in_enter_name)
        return await state.update_data(registration_message_id=callback.message_id, show_profile=True)

    await callback.message.answer(
        text=LEXICON['profile_message'].format(user.name, user.date_of_birth, user.status, user.phone_number),
        reply_markup=kb.start()
    )


@router.callback_query(F.data.startswith('cancel_payment_confirmation'))
async def cancel_payment_confirmation_handler(callback: CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split('_')[-1])

    await callback.message.delete()
    await callback.answer('Отправить подтверждение оплаты можно в разделе мероприятия', show_alert=True)

    registration = await db.get_registration(event_id, callback.from_user.id)
    await db.update_registration_status(registration.id, 'waiting_for_payment')

    await state.set_state(UserState.default_state)


# @router.callback_query(F.data.startswith('beer_pong_registration'))
# async def beer_pong_registration_handler(callback: CallbackQuery):
#     as_visitor = (callback.data.split('_')[-1] == 'visitor')
#
#     event = await db.get_event(BEER_PONG_EVENT_ID)
#
#     if as_visitor:
#         try:
#             await db.create_registration(BEER_PONG_EVENT_ID, callback.from_user.id)
#
#             return await callback.message.edit_text(
#                 LEXICON['registration_to_event_confirmed'].format(event.name, event.date)
#             )
#
#         except Exception as e:
#             print(f"\nОшибка при попытке регистрации пользователя {callback.from_user.id}\n{e}\n")
#             return await callback.message.edit_text(LEXICON['error_occurred'])
#
#     elif not await db.check_team_limit():
#         await callback.answer('К сожалению, места закончились', show_alert=True)
#         return await callback.message.edit_text(
#             text=LEXICON['event_info'].format(event.name, event.description, ''),
#             reply_markup=kb.beer_pong_registration_visitor()
#         )
#
#     await callback.message.edit_text(
#         text=LEXICON['beer_pong_registration_player'],
#         reply_markup=kb.beer_pong_registration_player()
#     )
#
#
# @router.callback_query(F.data.startswith('beer_pong_player'))
# async def beer_pong_player_handler(callback: CallbackQuery):
#     if callback.data.split('_')[-1] == 'registration':
#         invite_link = f'https://t.me/CUETA_events_bot?start=beer_pong_invite_{callback.from_user.id}'
#
#         return await callback.message.edit_text(
#             text=LEXICON['beer_pong_registrate_team'].format(invite_link)
#         )
#
#     try:
#         team = await db.join_team(callback.from_user.id, callback.from_user.username)
#         await db.create_registration(BEER_PONG_EVENT_ID, callback.from_user.id)
#     except Exception as e:
#         print(f"\nОшибка при попытке инициализации команды на бирпонг:\n{e}\n")
#         return await callback.message.edit_text(LEXICON['error_occurred'])
#
#     if team:
#         event = await db.get_event(BEER_PONG_EVENT_ID)
#
#         await callback.message.edit_text(
#             LEXICON['beer_pong_team_just_created'].format(event.name, team.player_1_username, team.id)
#         )
#
#         await bot.send_message(
#             chat_id=team.player_1_id,
#             text=LEXICON['beer_pong_team_just_created'].format(event.name, callback.from_user.username, team.id)
#         )
#
#     else:
#         try:
#             await callback.message.edit_text(LEXICON['beer_pong_solo'])
#         except Exception as e:
#             print(e)
#             await callback.message.edit_text(LEXICON['error_occurred'])


@router.message(F.text == buttons['help'])
async def help_button_handler(message: Message, state: FSMContext):
    await message.answer(LEXICON['help'])

    await state.set_state(UserState.default_state)


@router.message(F.text == buttons['profile'], IsNotRegistration())
async def profile_message_handler(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)

    if not (user.name and user.date_of_birth):
        message = await message.answer(LEXICON['you_need_to_sign_in'], reply_markup=kb.cancel_registration())

        await state.set_state(UserState.sign_in_enter_name)
        return await state.update_data(registration_message_id=message.message_id, show_profile=True)

    await message.answer(
        text=LEXICON['profile_message'].format(user.name, user.date_of_birth, user.status, user.phone_number),
        reply_markup=kb.start()
    )
