import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database import DataBase
from lexicon import LEXICON_RU, buttons, callbacks
from core import config


# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_linked_inline_kb(width: int,
                            **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for text, url in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                url=url))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    buttons.append(InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_menu"))
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_profile_inline_kb(width: int,
                             *args: str,
                             **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    kb_builder.adjust(2, 1, 2, 2)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_inline_kb_dict(width: int,
                          dict) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    for button, text in dict.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_menu_reply_kb(
        btn: list, ) -> ReplyKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[KeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if btn:
        for button in btn:
            buttons.append(KeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=2)
    kb_builder.adjust(2, 2, 2, 1)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_reply_kb(width: int,
                    btn: list, ) -> ReplyKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[KeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if btn:
        for button in btn:
            buttons.append(KeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


back_button: InlineKeyboardButton = InlineKeyboardButton(text=buttons['back'], callback_data=callbacks[buttons['back']])
admin_back_button: InlineKeyboardButton = InlineKeyboardButton(text=buttons['admin_back'],
                                                               callback_data=callbacks[buttons['admin_back']])


class StartKeyboards:
    def accept_user(self, user_id) -> InlineKeyboardMarkup:
        buttons = dict()
        buttons[f'user_accept_{user_id}'] = "✅ Принять"
        buttons[f'user_decline_{user_id}'] = "❌ Отклонить"
        return create_inline_kb_dict(2, buttons)


class UserKeyboards:
    menu = create_menu_reply_kb(
        [buttons['profile'], buttons['promo'],
         buttons['current_domain'], buttons['generators'],
         buttons['information'], buttons['contacts']]  # , buttons['tutors']]
    )

    def profile_kb(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            # InlineKeyboardButton(text='🆙 Повысить лимиты', callback_data=callbacks['🆙 Повысить лимиты']),
            # InlineKeyboardButton(text='📝 Изменить информацию', callback_data=callbacks['📝 Изменить информацию']),
            InlineKeyboardButton(text=buttons['link_wallet'], callback_data=callbacks[buttons['link_wallet']]),
            InlineKeyboardButton(text='💸 Запросить выплату', callback_data=callbacks['💸 Запросить выплату']),
            InlineKeyboardButton(text='⭐️ Установить никнейм', callback_data=callbacks['⭐️ Установить никнейм']),
            InlineKeyboardButton(text='🫂 Реферальная система', callback_data=callbacks['🫂 Реферальная система'])
        )
        kb.adjust(1, 2, 1)

        return kb.as_markup()

    def request_payout_ref(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text=buttons['request_payout_ref'],
                                    callback_data=callbacks[buttons['request_payout_ref']]))

        return kb.as_markup()

    def wallets(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text='BTC', callback_data=callbacks['BTC']),
            InlineKeyboardButton(text='ETH', callback_data=callbacks['ETH']),
            InlineKeyboardButton(text='USDT (TRC20)', callback_data=callbacks['USDT (TRC20)']),
            InlineKeyboardButton(text='TRX', callback_data=callbacks['TRX']),
            back_button
        )
        kb.adjust(2, 2)
        return kb.as_markup()

    def walets_for_payout(self, linked_wallets: dict) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for i in linked_wallets.keys():
            kb.add(InlineKeyboardButton(text=i, callback_data=f'payout_{i.lower()}'))
        kb.add(back_button)
        kb.adjust(2, 2, 1)

        return kb.as_markup()

    options = create_inline_kb_dict(2, {
        callbacks['🔗 Получить прокси']: '🔗 Получить прокси',
        callbacks['📱 Получить номер']: '📱 Получить номер',
        callbacks['📟 Генераторы']: '📟 Генераторы'
    })

    promo = create_inline_kb_dict(1, {
        callbacks['🔷 Получить промокод']: '🔷 Получить промокод',
        callbacks['📈 Статистика промокодов']: '📈 Статистика промокодов'
    })

    create_promo = create_inline_kb_dict(2, {
        callbacks[buttons['random_promo']]: buttons['random_promo'],
        callbacks[buttons['custom_promo']]: buttons['custom_promo'],
        callbacks[buttons['back']]: buttons['back']
    })

    tickers = create_inline_kb_dict(2, {
        'ticker_btc': '🟠 BTC',
        'ticker_eth': '🔷 ETH',
        'ticker_usdt': '🟢 TRC20',
        'ticker_trx': '🔻 TRX',
        callbacks[buttons['back']]: buttons['back']
    })

    def tutors(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text='📝 Заявка в филиал', callback_data=callbacks['📝 Заявка в филиал']))
        return kb.as_markup()

    def generators(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text=buttons['tags'], callback_data=callbacks[buttons['tags']]),
            InlineKeyboardButton(text='👧 Girls', callback_data=callbacks['👧 Girls']),
            InlineKeyboardButton(text='👻 NFT', callback_data=callbacks['👻 NFT']),
            InlineKeyboardButton(text=buttons['creo'], callback_data=callbacks[buttons['creo']])
        )
        kb.adjust(1, 2, 1, 1)

        return kb.as_markup()

    async def info(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text=buttons['workers_chat'], url=callbacks[buttons['workers_chat']]),
            InlineKeyboardButton(text=buttons['payments_channel'], url=callbacks[buttons['payments_channel']]),
            InlineKeyboardButton(text=buttons['info_channel'], url=callbacks[buttons['info_channel']])
        )
        kb.adjust(2, 1)
        return kb.as_markup()

    async def creo(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            InlineKeyboardButton(text=buttons['creo_yt_mr_beast'],
                                 callback_data=callbacks[buttons['creo_yt_mr_beast']]),
            InlineKeyboardButton(text=buttons['creo_PewDiePie'],
                                 callback_data=callbacks[buttons['creo_PewDiePie']]),
            InlineKeyboardButton(text=buttons['creo_poster_elon_musk'],
                                 callback_data=callbacks[buttons['creo_poster_elon_musk']]),
            back_button
        )
        kb.adjust(2, 1, 1)

        return kb.as_markup()

    def back(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(back_button)
        return kb.as_markup()


class AdminKeyboards:
    def super_menu(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text='📢 Рассылка', callback_data=callbacks['📢 Рассылка']),
            InlineKeyboardButton(text='➕ Добавить админа', callback_data=callbacks['➕ Добавить админа']),
            InlineKeyboardButton(text='🗑 Удалить админа', callback_data=callbacks['🗑 Удалить админа']),
            InlineKeyboardButton(text='🚫👶 Забанить пользователя', callback_data=callbacks['🚫👶 Забанить пользователя'])
        )
        kb.adjust(1, 2, 1)

        return kb.as_markup()

    def menu(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text='📢 Рассылка', callback_data=callbacks['📢 Рассылка']),
            InlineKeyboardButton(text='🚫👶 Забанить пользователя', callback_data=callbacks['🚫👶 Забанить пользователя'])
        )
        kb.adjust(1, 1)

        return kb.as_markup()

    async def back(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(admin_back_button)
        return kb.as_markup()

    async def delete_admin(self, self_id) -> InlineKeyboardMarkup:
        admins = await db.get_admins()
        kb = InlineKeyboardBuilder()
        for admin in admins:
            if admin.id == self_id:
                continue
            if admin.username:
                kb.row(InlineKeyboardButton(text=str(admin.username), callback_data=f'delete_admin_{str(admin.id)}'))
            else:
                kb.row(InlineKeyboardButton(text=str(admin.id), callback_data=f'delete_admin_{str(admin.id)}'))
        kb.adjust(2)
        kb.row(admin_back_button)
        return kb.as_markup()


class PaymentsKeyboard:
    async def payment(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(
                text=buttons['payment_accepted'],
                callback_data=callbacks[buttons['payment_accepted']])
        )

        return kb.as_markup()
