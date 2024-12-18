from typing import List

from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils import keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from lexicon import buttons, callbacks


class UserKeyboards:
    @staticmethod
    def start() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=buttons['upcoming_events'])],
                [KeyboardButton(text=buttons['profile']), KeyboardButton(text=buttons['help'])]
            ],
            resize_keyboard=True
        )

        return kb

    @staticmethod
    def profile() -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=buttons['change_profile_info'],
                                      callback_data=callbacks[buttons['change_profile_info']])]
            ]
        )

        return kb

    def change_profile_info(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=buttons['change_name'], callback_data=callbacks[buttons['change_name']]
                )],
                [InlineKeyboardButton(
                    text=buttons['change_date_of_birth'], callback_data=callbacks[buttons['change_date_of_birth']]
                )],
                [InlineKeyboardButton(
                    text=buttons['change_status'], callback_data=callbacks[buttons['change_status']]
                )],
                [InlineKeyboardButton(
                    text=buttons['change_phone_number'], callback_data=callbacks[buttons['change_phone_number']]
                )],
                [InlineKeyboardButton(
                    text=buttons['back'], callback_data=callbacks[buttons['back']]
                )]
            ]
        )

        return kb

    @staticmethod
    def menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['upcoming_events'], callback_data=callbacks[buttons['upcoming_events']]),
            InlineKeyboardButton(text=buttons['profile'], callback_data=callbacks[buttons['profile']]),
            InlineKeyboardButton(text=buttons['help'], callback_data=callbacks[buttons['help']])
        ).adjust(1, 2)

    @staticmethod
    def back_to_menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text=buttons['back_to_menu'], callback_data=callbacks[buttons['back_to_menu']])
        )

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
    def cancel_registration() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text=buttons['cancel_registration'], callback_data=callbacks['cancel_registration'])
        )

        return kb.as_markup()

    @staticmethod
    def enter_status() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['registration_status_bachelor-cu'],
                                 callback_data=callbacks[buttons['registration_status_bachelor-cu']]),
            InlineKeyboardButton(text=buttons['registration_status_master-cu'],
                                 callback_data=callbacks[buttons['registration_status_master-cu']]),
            InlineKeyboardButton(text=buttons['registration_status_other'],
                                 callback_data=callbacks[buttons['registration_status_other']])
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

    @staticmethod
    def beer_pong_registration() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['beer_pong_registration_visitor'],
                                 callback_data=callbacks[buttons['beer_pong_registration_visitor']]),
            InlineKeyboardButton(text=buttons['beer_pong_registration_player'],
                                 callback_data=callbacks[buttons['beer_pong_registration_player']])
        ).adjust(1)

        return kb.as_markup()

    @staticmethod
    def beer_pong_registration_visitor() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['beer_pong_registration_visitor'],
                                 callback_data=callbacks[buttons['beer_pong_registration_visitor']])
        )

        return kb.as_markup()

    @staticmethod
    def beer_pong_registration_player() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['beer_pong_player_team_registration'],
                                 callback_data=callbacks[buttons['beer_pong_player_team_registration']]),
            InlineKeyboardButton(text=buttons['beer_pong_player_team_creation'],
                                 callback_data=callbacks[buttons['beer_pong_player_team_creation']])
        ).adjust(1)

        return kb.as_markup()

    @staticmethod
    def beer_pong_cancel_registration_player(role: str) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text='❌ Отменить регистрацию',
                                 callback_data=callbacks['cancel_registration_on_beer_pong'])
        )

        return kb.as_markup()
