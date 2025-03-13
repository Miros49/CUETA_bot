from typing import List

from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from lexicon import buttons, callbacks


class UserKeyboards:
    @staticmethod
    def start() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=buttons["upcoming_events"])],
                [
                    KeyboardButton(text=buttons["profile"]),
                    KeyboardButton(text=buttons["help"]),
                ],
            ],
            resize_keyboard=True,
        )

        return kb

    # @staticmethod
    # def menu() -> InlineKeyboardMarkup:
    #     kb = InlineKeyboardBuilder()
    #     kb.add(
    #         InlineKeyboardButton(text=buttons['upcoming_events'], callback_data=callbacks[ ]),
    #         InlineKeyboardButton(text=buttons['profile'], callback_data=callbacks[buttons['profile']]),
    #         InlineKeyboardButton(text=buttons['help'], callback_data=callbacks[buttons['help']])
    #     ).adjust(1, 2)
    #
    # @staticmethod
    # def back_to_menu() -> InlineKeyboardMarkup:
    #     kb = InlineKeyboardBuilder()
    #     kb.row(
    #         InlineKeyboardButton(text=buttons['back_to_menu'], callback_data=callbacks[buttons['back_to_menu']])
    #     )

    @staticmethod
    def events_list(events: List[dict]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        for (
            event
        ) in events:  # TODO: добавлять мероприятие только если оно ещё не прошло
            kb.add(
                InlineKeyboardButton(
                    text=event["name"], callback_data=f"event_info_{event['id']}"
                )
            )

        return kb.adjust(1).as_markup()

    @staticmethod
    def register_to_event(
        event_id: int, show_registration: bool, show_payment_confirmation: bool = False
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        if show_registration:
            kb.add(
                InlineKeyboardButton(
                    text="Купить билет",
                    callback_data=callbacks[
                        buttons["event_registration_standard"]
                    ].format(event_id),
                ),
                # InlineKeyboardButton(
                #     text=buttons['event_registration_pre-registration'],
                #     callback_data=callbacks[buttons['event_registration_pre-registration']].format(event_id)
                # ),
                # InlineKeyboardButton(text=buttons['event_registration_premium'],
                #                      callback_data=callbacks[buttons['event_registration_premium']].format(event_id)),
                # InlineKeyboardButton(text=buttons['event_registration_fast'],
                #                      callback_data=callbacks[buttons['event_registration_fast']].format(event_id)),
            ).adjust(1)

        if show_payment_confirmation:
            kb.add(
                InlineKeyboardButton(
                    text=buttons["payment_confirmation_button"],
                    callback_data=callbacks[
                        buttons["payment_confirmation_button"]
                    ].format(event_id),
                )
            )

        kb.row(
            InlineKeyboardButton(
                text=buttons["back_button"],
                callback_data=callbacks[buttons["upcoming_events"]],
            )
        )

        return kb.as_markup()

    @staticmethod
    def confirm_payment(event_id: int):
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text=buttons["payment_confirmation_button"],
                callback_data=callbacks[buttons["payment_confirmation_button"]].format(
                    event_id
                ),
            )
        )

        return kb.as_markup()

    @staticmethod
    def cancel_payment_confirmation(event_id: int):
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data=callbacks["cancel_payment_confirmation_button"].format(
                    event_id
                ),
            )
        )

        return kb.as_markup()

    @staticmethod
    def cancel_registration() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=buttons["cancel_registration"],
                callback_data=callbacks[buttons["cancel_registration"]],
            )
        )

        return kb.as_markup()

    @staticmethod
    def profile_registration_back_to_name() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=buttons["back_button"],
                callback_data=callbacks["profile_registration_back_to_name"],
            )
        )

        return kb.as_markup()

    @staticmethod
    def profile_registration_back_to_status() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=buttons["back_button"],
                callback_data=callbacks["profile_registration_back_to_status"],
            )
        )

        return kb.as_markup()

    @staticmethod
    def enter_status() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text=buttons["registration_status_bachelor-cu"],
                callback_data=callbacks[buttons["registration_status_bachelor-cu"]],
            ),
            InlineKeyboardButton(
                text=buttons["registration_status_master-cu"],
                callback_data=callbacks[buttons["registration_status_master-cu"]],
            ),
            # InlineKeyboardButton(text=buttons['registration_status_t-bank'],
            #                      callback_data=callbacks[buttons['registration_status_t-bank']]),
            InlineKeyboardButton(
                text=buttons["registration_status_other"],
                callback_data=callbacks[buttons["registration_status_other"]],
            ),
            InlineKeyboardButton(
                text=buttons["back_button"],
                callback_data=callbacks["profile_registration_back_to_date_of_birth"],
            ),
        ).adjust(2, 1)

        return kb.as_markup()

    @staticmethod
    def request_phone_number() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Отправить", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

        return kb

    @staticmethod
    def confirm_registration() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=buttons["confirm_registration"],
                callback_data=callbacks[buttons["confirm_registration"]],
            ),
            InlineKeyboardButton(
                text=buttons["cancel_registration"],
                callback_data=callbacks[buttons["cancel_registration"]],
            ),
            InlineKeyboardButton(
                text=buttons["back_button"],
                callback_data=callbacks["profile_registration_back_to_phone_number"],
            ),
        ).adjust(2)

        return kb.as_markup()

    @staticmethod
    def profile_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons["top_up_balance"],callback_data=callbacks[buttons["top_up_balance"]]),
            InlineKeyboardButton(text=buttons['change_profile'], callback_data=callbacks[buttons['change_profile']])
        ).adjust(1)

        return kb.as_markup()

    @staticmethod
    def change_profile_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['change_name'],
                                 callback_data=callbacks[buttons['change_name']]),
            # InlineKeyboardButton(text=buttons['change_date_of_birth'], callback_data=callbacks[buttons['change_date_of_birth']]), # TODO: Смена даты рождения?
            InlineKeyboardButton(text=buttons['change_phone_number'],
                                 callback_data=callbacks[buttons['change_phone_number']]),
            InlineKeyboardButton(text=buttons['change_status'],
                                 callback_data=callbacks[buttons['change_status']]),
            InlineKeyboardButton(text=buttons['back_button'],
                                 callback_data=callbacks['back_to_profile'])
        ).adjust(1)

        return kb.as_markup()

    @staticmethod
    def change_name_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['back_button'],
                                 callback_data=callbacks['back_to_profile'])
        )

        return kb.as_markup()

    @staticmethod
    def change_status_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['registration_status_bachelor-cu'],
                                 callback_data=callbacks[buttons['registration_status_bachelor-cu']]),
            InlineKeyboardButton(text=buttons['registration_status_master-cu'],
                                 callback_data=callbacks[buttons['registration_status_master-cu']]),
            # InlineKeyboardButton(text=buttons['registration_status_t-bank'],
            #                      callback_data=callbacks[buttons['registration_status_t-bank']]),
            InlineKeyboardButton(text=buttons['registration_status_other'],
                                 callback_data=callbacks[buttons['registration_status_other']]),
            InlineKeyboardButton(text=buttons['back_button'],
                                 callback_data=callbacks['back_to_profile'])
        ).adjust(2, 1)

        return kb.as_markup()

    @staticmethod
    def coins_amount_kb() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text="1", callback_data=callbacks["enter_coins_amount"].format(1)
            ),
            InlineKeyboardButton(
                text="3", callback_data=callbacks["enter_coins_amount"].format(3)
            ),
            InlineKeyboardButton(
                text="5", callback_data=callbacks["enter_coins_amount"].format(5)
            ),
            InlineKeyboardButton(
                text="10", callback_data=callbacks["enter_coins_amount"].format(10)
            ),
            InlineKeyboardButton(
                text="Ввести вручную",
                callback_data=callbacks["enter_coins_amount"].format("manual"),
            ),
            InlineKeyboardButton(
                text=buttons["back_button"], callback_data=callbacks["back_to_profile"]
            ),
        ).adjust(2, 2, 1)

        return kb.as_markup()

    @staticmethod
    def back_to_top_up_menu() -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=buttons["back_button"],
                callback_data=callbacks[buttons["top_up_balance"]],
            )
        )

        return kb.as_markup()

    @staticmethod
    def confirm_transaction(transaction_id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text=buttons["payment_confirmation_button"],
                callback_data=callbacks["confirm_transaction"].format(transaction_id),
            ),
            InlineKeyboardButton(
                text="❌ Отменить",
                callback_data=callbacks["cancel_transaction"].format(transaction_id),
            ),
        ).adjust(1)

        return kb.as_markup()

    @staticmethod
    def cancel_transaction(transaction_id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text="❌ Отменить",
                callback_data=callbacks["cancel_transaction"].format(transaction_id),
            )
        )

        return kb.as_markup()


class FundraiserKeyboards:  # TODO: вынести в отдельный файл
    @staticmethod
    def confirm_payment(registration_id: int):
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text="✅ Подтвердить",
                callback_data=f"fundraiser_payment_confirmation_confirm_{registration_id}",
            ),
            InlineKeyboardButton(
                text="❌ Фигню вкинул",
                callback_data=f"fundraiser_payment_confirmation_cancel_{registration_id}",
            ),
        )

        return kb.as_markup()

    @staticmethod
    def confirm_transaction(transaction_id: int):
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(
                text="✅ Подтвердить",
                callback_data=f"fundraiser_transaction_confirmation_confirm_{transaction_id}",
            ),
            InlineKeyboardButton(
                text="❌ Фигню вкинул",
                callback_data=f"fundraiser_transaction_confirmation_cancel_{transaction_id}",
            ),
        )

        return kb.as_markup()
