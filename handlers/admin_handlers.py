import asyncio

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
async def admin_menu_callback_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON['admin_menu'].format(callback.from_user.first_name),
                                     reply_markup=kb.menu())

    await state.set_state(AdminState.default_state)


@router.callback_query(F.data == callbacks[buttons['admin_mailing']])
async def mailing_handler(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON['admin_mailing_options'], reply_markup=kb.mailing_options())


@router.callback_query(F.data.startswith('admin_mailing_options'))
async def admin_mailing_options_callback_handler(callback: CallbackQuery, state: FSMContext):
    additional_message = await callback.message.edit_text(LEXICON['admin_enter_mailing_message'])

    await state.set_state(AdminState.enter_mailing_message)
    await state.update_data(additional_message_id=additional_message.message_id)


@router.message(StateFilter(AdminState.enter_mailing_message))
async def enter_mailing_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.delete()
    await bot.delete_message(message.chat.id, data['additional_message_id'])

    if message.text:
        message_type = 'text'
        item = message.text
        caption = None

    elif message.photo:
        message_type = 'photo'
        item = message.photo[0].file_id
        caption = message.caption if message.caption else ''

    elif message.video:
        message_type = 'video'
        item = message.video.file_id
        caption = message.caption if message.caption else ''

    elif message.sticker:
        message_type = 'sticker'
        item = message.sticker.file_id
        caption = None

    elif message.voice:
        message_type = 'voice'
        item = message.voice.file_id
        caption = message.caption if message.caption else '⠀'

    elif message.video_note:
        message_type = 'video_note'
        item = message.video_note.file_id
        caption = None

    elif message.animation:
        message_type = 'animation'
        item = message.animation.file_id
        caption = message.caption if message.caption else ''

    else:
        await bot.delete_message(message.chat.id, message.message_id)
        mes = await message.answer('Извините, на данный момент данный тип сообщений не поддерживается')
        await asyncio.sleep(2)
        return await mes.delete()

    send_method = {
        'text': bot.send_message,
        'photo': bot.send_photo,
        'video': bot.send_video,
        'sticker': bot.send_sticker,
        'voice': bot.send_voice,
        'video_note': bot.send_video_note,
        'animation': bot.send_animation,
    }

    if message_type == 'text':
        await send_method[message_type](message.from_user.id, item, disable_web_page_preview=True,
                                        reply_markup=kb.confirm_mailing())

    elif not caption:
        await send_method[message_type](message.from_user.id, item)

    else:
        await send_method[message_type](message.from_user.id, item, caption=caption, reply_markup=kb.confirm_mailing())

    await state.set_state(AdminState.default_state)
    await state.update_data(message_type=message_type, item=item, caption=caption)


@router.callback_query(F.data == callbacks[buttons['initiate_mailing']])
async def initiate_mailing_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id, message_id=callback.message.message_id,
        reply_markup=None
    )

    if not (data.get('message_type') and data.get('item')):
        print(data)
        return await callback.answer('Для этого вам необходимо заново инициализировать рассылку', show_alert=True)
    else:
        mes = await callback.message.answer('⏳ Начинаю рассылку...')

    message_type, item, caption = data.get('message_type'), data.get('item'), data.get('caption', None)

    send_method = {
        'text': bot.send_message,
        'photo': bot.send_photo,
        'video': bot.send_video,
        'sticker': bot.send_sticker,
        'voice': bot.send_voice,
        'video_note': bot.send_video_note,
        'animation': bot.send_animation,
    }

    print(len(await db.get_event_registrations(1)), '\n\n', await db.get_event_registrations(1))

    for user_id in await db.get_event_registrations(1):
        try:
            if not caption:
                await send_method[message_type](user_id, item, disable_web_page_preview=True)
            else:
                await send_method[message_type](user_id, item, caption=caption)

            await asyncio.sleep(0.1)  # задержка чтоб не заблокировали

        except TelegramBadRequest:
            pass

        except TelegramForbiddenError:
            pass

        except Exception:
            pass

    await mes.edit_text('✅ Рассылка завершена!')


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


@router.message(F.text == 'списки')
async def send_registrations_list(message: Message):
    if message.from_user.id in config.tg_bot.admin_ids:
        file_path = await db.generate_registration_report(1)
        file = FSInputFile(file_path)

        await message.answer_document(file)


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

    await callback.message.edit_text(LEXICON['admin_event_creation_canceled'], reply_markup=kb.back_to_menu())


# @router.message(F.text == 'рассылка')  # TODO: это временное решение. нужно убрать этот колхоз
# async def beer_pong_mailing_handler(message: Message):
#     form_link = ('https://docs.google.com/forms/d/15n5kIpaH1zOaPWjkyCqOSBO67uUOmnKlGznhfihVX20/'
#                  'viewform?edit_requested=true')
#     text = (
#         'Спасибо, что провёл вечер с нами! 😉\n\n'
#         '<b>Наша цель</b> — создавать для тебя яркие моменты и помогать ощутить себя частью '
#         'большого студенческого сообщества.\n\n'
#         '<b>Расскажи как все прошло для тебя!</b> Твое мнение поможет нам стать еще лучше.'
#         f'<b>Создали для тебя <a href="{form_link}">короткую форму</a></b>'
#     )


def todo() -> None:
    # TODO: вместо кнопки помощь "по вопросам пишите туда"
    return None
