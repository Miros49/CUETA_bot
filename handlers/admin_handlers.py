import asyncio
from datetime import datetime, timedelta

from aiogram import F, Router, exceptions
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from core import bot, config
from database import db, Registration
from filters import IsAdmin
from keyboards import AdminKeyboards, UserKeyboards
from lexicon import LEXICON, callbacks, buttons
from states import AdminState, UserState
from utils import convert_string_to_date, get_user_state
from utils.utils import is_user_adult

router: Router = Router()
kb: AdminKeyboards = AdminKeyboards()
user_kb: UserKeyboards = UserKeyboards()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("admin"))
async def admin_menu_handler(message: Message, state: FSMContext):
    menu_message = LEXICON["admin_menu"].format(message.from_user.first_name)

    # Получаем статистику
    statistics = await db.get_registration_statistics()

    # Формируем сообщение для общей статистики
    overall_statistics_message = LEXICON["admin_overall_statistics"].format(
        total=statistics["overall_statistics"]["total"],
        confirmed=statistics["overall_statistics"]["confirmed"],
        waiting_for_confirmation=statistics["overall_statistics"][
            "waiting_for_confirmation"
        ],
        waiting_for_payment=statistics["overall_statistics"]["waiting_for_payment"],
        ready_to_pay=statistics["overall_statistics"]["ready_to_pay"],
        processing=statistics["overall_statistics"]["processing"],
    )

    # Формируем сообщения для каждого сборщика
    fundraisers_statistics_messages = [
        LEXICON["admin_fundraiser_statistics"].format(
            fundraiser_username=fundraiser["fundraiser_username"],
            collected_money=fundraiser["collected_money"],
            total=fundraiser["total"],
            confirmed=fundraiser["confirmed"],
            waiting_for_confirmation=fundraiser["waiting_for_confirmation"],
            waiting_for_payment=fundraiser["waiting_for_payment"],
            ready_to_pay=fundraiser["ready_to_pay"],
        )
        for fundraiser in statistics["fundraisers_statistics"]
    ]

    # Объединяем сообщения
    full_message = (
        f"{menu_message}\n\n"
        f"{overall_statistics_message}\n\n"
        f"<b>📊 Статистика по сборщикам:</b>\n\n"
        f"{''.join(fundraisers_statistics_messages)}"
    )

    # Отправляем сообщение с клавиатурой
    await message.answer(full_message, reply_markup=kb.menu())

    # Устанавливаем состояние
    await state.set_state(AdminState.default_state)


@router.callback_query(F.data == callbacks[buttons["admin_back_to_menu"]])
async def admin_menu_callback_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        LEXICON["admin_menu"].format(callback.from_user.first_name),
        reply_markup=kb.menu(),
    )

    await state.set_state(AdminState.default_state)


@router.callback_query(F.data == callbacks[buttons["admin_mailing"]])
async def mailing_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        LEXICON["admin_mailing_options"], reply_markup=kb.mailing_options()
    )


@router.callback_query(F.data.startswith("admin_mailing_options"))
async def admin_mailing_options_callback_handler(
    callback: CallbackQuery, state: FSMContext
):
    additional_message = await callback.message.edit_text(
        LEXICON["admin_enter_mailing_message"]
    )

    await state.set_state(AdminState.enter_mailing_message)
    await state.update_data(additional_message_id=additional_message.message_id)


@router.message(StateFilter(AdminState.enter_mailing_message))
async def enter_mailing_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()
    await bot.delete_message(message.chat.id, data["additional_message_id"])

    if message.text:
        message_type = "text"
        item = message.text
        caption = None

    elif message.photo:
        message_type = "photo"
        item = message.photo[0].file_id
        caption = message.caption if message.caption else ""

    elif message.video:
        message_type = "video"
        item = message.video.file_id
        caption = message.caption if message.caption else ""

    elif message.sticker:
        message_type = "sticker"
        item = message.sticker.file_id
        caption = None

    elif message.voice:
        message_type = "voice"
        item = message.voice.file_id
        caption = message.caption if message.caption else "⠀"

    elif message.video_note:
        message_type = "video_note"
        item = message.video_note.file_id
        caption = None

    elif message.animation:
        message_type = "animation"
        item = message.animation.file_id
        caption = message.caption if message.caption else ""

    else:
        await bot.delete_message(message.chat.id, message.message_id)
        mes = await message.answer(
            "Извините, на данный момент данный тип сообщений не поддерживается"
        )
        await asyncio.sleep(2)
        return await mes.delete()

    send_method = {
        "text": bot.send_message,
        "photo": bot.send_photo,
        "video": bot.send_video,
        "sticker": bot.send_sticker,
        "voice": bot.send_voice,
        "video_note": bot.send_video_note,
        "animation": bot.send_animation,
    }

    if message_type == "text":
        await send_method[message_type](
            message.from_user.id,
            item,
            disable_web_page_preview=True,
            reply_markup=kb.confirm_mailing(),
        )

    elif not caption:
        await send_method[message_type](message.from_user.id, item)

    else:
        await send_method[message_type](
            message.from_user.id,
            item,
            caption=caption,
            reply_markup=kb.confirm_mailing(),
        )

    await state.set_state(AdminState.default_state)
    await state.update_data(message_type=message_type, item=item, caption=caption)


@router.callback_query(F.data == callbacks[buttons["initiate_mailing"]])
async def initiate_mailing_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None,
    )

    if not (data.get("message_type") and data.get("item")):
        print(data)
        return await callback.answer(
            "Для этого вам необходимо заново инициализировать рассылку", show_alert=True
        )
    else:
        mes = await callback.message.answer("⏳ Начинаю рассылку...")

    message_type, item, caption = (
        data.get("message_type"),
        data.get("item"),
        data.get("caption", None),
    )

    send_method = {
        "text": bot.send_message,
        "photo": bot.send_photo,
        "video": bot.send_video,
        "sticker": bot.send_sticker,
        "voice": bot.send_voice,
        "video_note": bot.send_video_note,
        "animation": bot.send_animation,
    }

    print(
        len(await db.get_event_registrations(1)),
        "\n\n",
        await db.get_event_registrations(1),
    )

    for user_id in await db.get_event_registrations(1):
        try:
            if not caption:
                await send_method[message_type](
                    user_id, item, disable_web_page_preview=True
                )
            else:
                await send_method[message_type](user_id, item, caption=caption)

            await asyncio.sleep(0.1)  # задержка чтоб не заблокировали

        except TelegramBadRequest:
            pass

        except TelegramForbiddenError:
            pass

        except Exception as e:
            print(f"Некритическая ошибка при попытке рассылки: {e}")
            pass

    await mes.edit_text("✅ Рассылка завершена!")


@router.callback_query(F.data == callbacks[buttons["admin_events"]])
async def events_handler(callback: CallbackQuery):
    events = await db.get_upcoming_events()

    await callback.message.edit_text(
        LEXICON["events_list"], reply_markup=kb.upcoming_events(events)
    )


@router.callback_query(F.data == callbacks[buttons["admin_create_event"]])
async def admin_create_event_callback_handler(
    callback: CallbackQuery, state: FSMContext
):
    message = await callback.message.edit_text(LEXICON["admin_add_event_name"])

    await state.set_state(AdminState.enter_event_name)
    await state.update_data(event_creation_message_id=message.message_id)


@router.message(StateFilter(AdminState.enter_event_name))
async def event_name_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["event_creation_message_id"],
        text=LEXICON["admin_add_event_description"].format(message.text),
    )

    await state.set_state(AdminState.enter_event_description)
    await state.update_data(event_name=message.text)


@router.message(StateFilter(AdminState.enter_event_description))
async def event_description_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["event_creation_message_id"],
        text=LEXICON["admin_add_event_date"].format(data["event_name"], message.text),
    )

    await state.set_state(AdminState.enter_event_date)
    await state.update_data(event_description=message.text)


@router.message(StateFilter(AdminState.enter_event_date))
async def event_date_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()  # TODO: нужно проверять дату на правильность ввода + добавить везде кнопки "назад"

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=data["event_creation_message_id"],
        text=LEXICON["admin_add_event_card"].format(
            data["event_name"], data["event_description"], message.text
        ),
    )

    await state.update_data(event_date=message.text)
    await state.set_state(AdminState.enter_event_card)


@router.message(StateFilter(AdminState.enter_event_card))
async def event_card_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()

    if not message.photo:
        return await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=data["event_creation_message_id"],
            text=LEXICON["admin_add_event_card"].format(
                data["event_name"], data["event_description"], data["event_date"]
            ),
        )

    await bot.delete_message(
        chat_id=message.chat.id, message_id=data["event_creation_message_id"]
    )
    await message.answer_photo(
        photo=message.photo[-1].file_id,
        caption=LEXICON["admin_create_event"].format(
            data["event_name"], data["event_description"], data["event_date"]
        ),
        reply_markup=kb.confirm_creation_of_event(),
    )

    await state.update_data(event_photo_id=message.photo[-1].file_id)
    await state.set_state(AdminState.default_state)


@router.callback_query(
    F.data.in_(
        [
            callbacks[buttons["admin_creation_of_event_confirm"]],
            callbacks[buttons["admin_creation_of_event_cancel"]],
        ]
    )
)
async def create_event_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if callback.data.split("_")[-1] != "confirm":
        await callback.message.edit_text(
            LEXICON["admin_event_creation_canceled"], reply_markup=kb.back_to_menu()
        )

    try:
        event_date = await convert_string_to_date(data["event_date"])

        await db.create_event(
            data["event_name"],
            data["event_description"],
            event_date,
            data["event_photo_id"],
        )

    except Exception as e:
        print(f"Ошибка при попытке создания мероприятия: {e}")

        return await callback.message.answer(LEXICON["error_occurred"])

    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON["admin_event_created"].format(
                data["event_name"], data["event_description"], data["event_date"]
            ),  # TODO: сюда кнопку удаления мероприятия
        )
    else:
        await callback.message.edit_text(
            text=LEXICON["admin_event_created"].format(
                data["event_name"], data["event_description"], data["event_date"]
            ),  # TODO: и сюда
        )

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


@router.message(F.text == "списки")
async def send_registrations_list(message: Message):
    if message.from_user.id in config.tg_bot.admin_ids:
        file_path = await db.generate_registration_report(1)
        file = FSInputFile(file_path)

        await message.answer_document(file)


# @router.message(F.text == 'предрега')
# async def send_registrations_list(message: Message):
#     event = await db.get_event(event_id=2)
#     registration_type = 'pre-registration'
#     user_ids = await db.get_user_ids_from_registrations(event_id=event.id, registration_type=registration_type)
#
#     print(user_ids)
#
#     for user_id in user_ids:
#         user = await db.get_user(user_id)
#         registration = await db.get_registration(event.id, user_id)
#
#         if not (user.name and user.date_of_birth):
#             try:
#                 await bot.send_message(
#                     chat_id=user_id,
#                     text=LEXICON['pre-registration_mailing_no_profile'],
#                     disable_web_page_preview=True
#                 )
#
#                 pre_registration_message = await bot.send_message(
#                     chat_id=user_id,
#                     text=LEXICON['enter_your_name'],
#                 )
#
#                 state = get_user_state(user.id)
#                 await state.set_state(UserState.sign_in_enter_name)
#                 await state.update_data(
#                     registration_message_id=pre_registration_message.message_id,
#                     pre_registration_filling_profile=True
#                 )
#                 continue
#
#             except Exception as e:
#                 await manual_registration(user_id, registration, e)
#                 continue
#
#         try:
#             fundraiser = await db.get_fundraiser_with_least_registrations()
#
#             try:
#                 await db.assign_fundraiser_to_registration(registration.id, fundraiser.id)
#                 await db.assign_fundraiser_to_registration(registration.id, fundraiser.id)
#                 await db.increment_registration_count(fundraiser.id)
#                 await db.update_registration_status(registration.id, 'waiting_for_payment')
#
#             except Exception as e:
#                 await manual_registration(user_id, registration, e)
#                 continue
#
#             print(
#                 f'FUNDRAISER {fundraiser.username} assigned for registration {registration.id} '
#                 f'({("@" + registration.username) if registration.username else registration.user_id})\n'
#                 f'{(datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")}\n'
#             )
#
#             await db.set_first_warning(registration.id)
#
#         except Exception as e:
#             await manual_registration(user_id, registration, e)
#             continue
#
#         fundraiser = await db.get_fundraiser(registration.fundraiser_id)
#
#         text = LEXICON['pre-registration_mailing'].format(fundraiser.phone_number, fundraiser.preferred_bank,
#                                                           fundraiser.username) if is_user_adult(user.date_of_birth) \
#             else LEXICON['pre-registration_mailing_underage'].format(
#             fundraiser.username, fundraiser.phone_number, fundraiser.preferred_bank, fundraiser.username
#         )
#
#         try:
#             await bot.send_message(
#                 chat_id=user_id, text=text,
#                 reply_markup=user_kb.register_to_event(event.id, False, True),
#                 disable_web_page_preview=True
#             )
#
#         except Exception as e:
#             await manual_registration(user_id, registration, e)
#             continue
#
#         await asyncio.sleep(0.15)  # задержка чтоб не заблокировали
#
#     await message.answer('Готово')


async def manual_registration(user_id: int, registration: Registration, error):
    await asyncio.sleep(0.1)

    await bot.send_message(
        chat_id=922787101,
        text=(
            f"Необходимо лично связаться с "
            f"{('@' + registration.username) if registration.username else registration.user_id}\n"
            f"ID регистрации: <code>{registration.id}</code>"
            f"{(datetime.utcnow() + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M:%S')}\n"
        ),
    )

    await asyncio.sleep(0.1)

    try:
        await bot.send_message(
            chat_id=user_id,
            text="<b>К сожалению, не смогли подобрать для вас сборщика из-за высокой нагрузки.\n"
            "Скоро свяжемся с тобой! 🤗</b>",
        )
    except Exception as e:
        print(e)

    return print(f"необходимо лично связаться с типом. ошибка: {error}")


# @router.message(F.text == 'рассылка даунам')
# async def test_handler(message: Message):
#     users_ids = await db.get_users_with_specific_status_and_warning()
#     counter = 0
#
#     print(len(users_ids), '\n', users_ids)
#
#     for user_id in users_ids:
#         user = await db.get_user(user_id)
#         registration = await db.get_registration(2, user_id)
#         fundraiser = await db.get_fundraiser(registration.fundraiser_id)
#
#         if is_user_adult(user.date_of_birth):
#             text = LEXICON['temp_mailing_mexican_party'].format(
#                 fundraiser.phone_number, fundraiser.preferred_bank, fundraiser.username
#             )
#         else:
#             text = LEXICON['temp_mailing_mexican_party_underage'].format(
#                 fundraiser.username, fundraiser.phone_number, fundraiser.preferred_bank, fundraiser.username
#             )
#
#         try:
#             await bot.send_message(
#                 chat_id=user_id, text=text,
#                 reply_markup=user_kb.register_to_event(2, False, True),
#                 disable_web_page_preview=True
#             )
#             counter += 1
#
#         except Exception as e:
#             print(e)
#
#         await asyncio.sleep(0.1)
#
#     await message.answer(f'Готово!\n{counter} из {len(users_ids)}')


@router.message(F.text == "рассылка даунам")
async def mailing_handler(message: Message):
    unregistered_users_ids = await db.get_unregistered_users()
    users_with_unconfirmed_status = await db.get_users_with_unconfirmed_status()

    print(len(unregistered_users_ids), "\n", unregistered_users_ids)
    print(len(users_with_unconfirmed_status), "\n", users_with_unconfirmed_status)
    print(
        len(
            set(unregistered_users_ids).intersection(set(users_with_unconfirmed_status))
        )
    )

    users_ids = list(set(unregistered_users_ids) | set(users_with_unconfirmed_status))
    counter = 0

    for user_id in users_ids:
        text = (
            "<b>Стипендия пришла, а билет ещё не купил? 🤔</b>\n\n"
            "Осталось всего <b>45 минут</b> до повышения цены! 🎟🔥\n"
            "Самое время порадовать себя — вложи в <i>яркие эмоции</i> и <b>незабываемый старт семестра</b>! 🎉\n\n"
            "<b>Скоро будет дороже</b>, так что не откладывай — успей забрать билет сейчас! 👇\n\n"
            "<i>При возникновении технических проблем, просим обратиться к нашим администраторам:</i>\n"
            "👨‍💻 @ShIN_66 | @Miros49"
        )

        try:
            await bot.send_message(chat_id=user_id, text=text)
            counter += 1

        except TelegramBadRequest:
            pass

        except TelegramForbiddenError:
            pass

        except Exception as e:
            print(f"Некритическая ошибка при попытке рассылки: {e}")
            pass

        await asyncio.sleep(0.1)

    await message.answer(f"Готово!\n{counter} из {len(users_ids)}")
