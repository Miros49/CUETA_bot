from typing import List

from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from lexicon import buttons, callbacks


class UserKeyboards:
    @staticmethod
    def start() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['upcoming_events'], callback_data=callbacks[buttons['upcoming_events']]),
            InlineKeyboardButton(text=buttons['help'], callback_data=callbacks[buttons['help']])
        ).adjust(1, 2)

        return kb.as_markup()

    @staticmethod
    def events_list(events: List[dict]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for event in events:  # TODO: добавлять мероприятие только если оно ещё не прошло
            kb.add(InlineKeyboardButton(text=event['name'], callback_data=f'event_info_{event["id"]}'))

        return kb.as_markup()

    @staticmethod
    def register_to_event(event_id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['event_registration_standard'],
                                 callback_data=callbacks[buttons['event_registration_standard']].format(event_id)),
            InlineKeyboardButton(text=buttons['event_registration_fast'],
                                 callback_data=callbacks[buttons['event_registration_fast']].format(event_id))
        ).adjust(1)

        return kb.as_markup()

    @staticmethod
    def request_phone_number() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Отправить", request_contact=True)]],
            resize_keyboard=True, one_time_keyboard=True
        )

        return kb

    @staticmethod
    def confirm_registration() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text=buttons['confirm_registration'],
                                 callback_data=callbacks[buttons['confirm_registration']]),
            InlineKeyboardButton(text=buttons['cancel_registration'],
                                 callback_data=callbacks[buttons['cancel_registration']])
        )

        return kb.as_markup()
