from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import buttons, callbacks


class AdminKeyboards:
    @staticmethod
    def menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text=buttons['admin_mailing'], callback_data=callbacks[buttons['admin_mailing']]),
            InlineKeyboardButton(text=buttons['admin_events'], callback_data=callbacks[buttons['admin_events']])
        )
        kb.adjust(1, 1)

        return kb.as_markup()

    @staticmethod
    def back_to_menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text=buttons['admin_back_to_menu'],
                                    callback_data=callbacks[buttons['admin_back_to_menu']]))

        return kb.as_markup()

    @staticmethod
    def upcoming_events(events: List[dict]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for event in events:  # TODO: добавлять мероприятие только если оно ещё не прошло
            kb.add(InlineKeyboardButton(text=event['name'], callback_data=f'admin_event_{event["id"]}'))

        kb.row(
            InlineKeyboardButton(text=buttons['admin_create_event'],
                                 callback_data=callbacks[buttons['admin_create_event']]))

        return kb.as_markup()

    @staticmethod
    def confirm_creation_of_event():
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text=buttons['admin_creation_of_event_confirm'],
                                 callback_data=callbacks[buttons['admin_creation_of_event_confirm']]),
            InlineKeyboardButton(text=buttons['admin_creation_of_event_cancel'],
                                 callback_data=callbacks[buttons['admin_creation_of_event_cancel']])
        )

        return kb.as_markup()
