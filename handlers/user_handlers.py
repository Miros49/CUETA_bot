from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext

from core import config
from database import db
from keyboards import UserKeyboards
from lexicon import *
from states import UserState
from utils import *

router: Router = Router()
kb = UserKeyboards()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer('Салам')


@router.callback_query(F.data == callbacks[buttons['back']])
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if not current_state or current_state == UserState.enter_nickname:
        if callback.message.text == LEXICON_RU['select_generator']:
            await callback.message.edit_text(LEXICON_RU['tools_for_work'], reply_markup=kb.options)
        elif callback.message.text == LEXICON_RU['enter_promo']:
            text = LEXICON_RU['your_promo']
            user = await db.get_promocodes(callback.from_user.id)
            if not user or not user.promocodes:
                if not user:
                    await db.set_user_promocodes(callback.from_user.id)
                text += 'У Вас ещё нет промокодов'
            elif user.promocodes:
                text += '▪️<code>' + '</code>\n▪️<code>'.join(user.promocodes.split(',')) + '</code>'

            await callback.message.edit_text(text, reply_markup=kb.promo, parse_mode='HTML')
        elif callback.message.text == '🔥 CREO:':
            await callback.message.edit_text(LEXICON_RU['select_generator'], reply_markup=kb.generators())
        elif callback.message.text == LEXICON_RU['promo_type']:
            text = LEXICON_RU['your_promo']
            user = await db.get_promocodes(callback.from_user.id)
            if not user or not user.promocodes:
                if not user:
                    await db.set_user_promocodes(callback.from_user.id)
                text += 'У Вас ещё нет промокодов'
            elif user.promocodes:
                text += '▪️<code>' + '</code>\n▪️<code>'.join(user.promocodes.split(',')) + '</code>'

            await callback.message.edit_text(text, reply_markup=kb.promo, parse_mode='HTML')
        elif callback.message.text == LEXICON_RU['promo_ticker']:
            await callback.message.edit_text(LEXICON_RU['promo_type'], reply_markup=kb.create_promo)
        else:
            user = await db.get_user(callback.from_user.id)
            wallets = await db.get_wallets(callback.from_user.id)
            await callback.message.edit_text(LEXICON_RU['profile'].format(
                user_id=callback.from_user.id,
                nickname=f"<code>{user.nickname}</code>" if user and user.nickname else 'Нет',
                lolz=user.lolz_profile if user.lolz_profile else 'Нет профиля',
                tutor='Отсутствует',
                status=user.status,
                current_balance=str(user.balance),
                total_turnover=str(user.total_turnover),
                percent=str(await get_percent(user.total_turnover)),
                users_count=user.users_count,
                btc=f"<code>{wallets.btc}</code>" if wallets and wallets.btc else 'Не привязан',
                eth=f"<code>{wallets.eth}</code>" if wallets and wallets.eth else 'Не привязан',
                trc20=f"<code>{wallets.trc20}</code>" if wallets and wallets.trc20 else 'Не привязан',
                tron=f"<code>{wallets.trx}</code>" if wallets and wallets.trx else 'Не привязан'
            ), reply_markup=kb.profile_kb(), parse_mode='HTML')
    elif current_state == UserState.generate_tags:
        await callback.message.edit_text(LEXICON_RU['select_generator'], reply_markup=kb.generators())
    elif current_state == UserState.enter_promo:
        await callback.message.edit_text(LEXICON_RU['your_promo'], reply_markup=kb.promo)
    elif current_state == UserState.enter_payout_amount:
        linked_wallets = await db.get_linked_wallets(callback.from_user.id)
        await callback.message.edit_text(LEXICON_RU['choose_wallet_for_payout'],
                                         reply_markup=kb.walets_for_payout(linked_wallets))
    await state.clear()


@router.message(F.text == buttons['profile'])
async def profile(message: Message):
    user = await db.get_user(message.from_user.id)
    wallets = await db.get_wallets(message.from_user.id)
    await message.answer(LEXICON_RU['profile'].format(
        user_id=message.from_user.id,
        nickname=f"<code>{user.nickname}</code>" if user and user.nickname else 'Нет',
        lolz=user.lolz_profile if user.lolz_profile else 'Нет профиля',
        tutor='Отсутствует',
        status=user.status,
        current_balance=str(user.balance),
        total_turnover=str(user.total_turnover),
        percent=str(await get_percent(user.total_turnover)),
        users_count=user.users_count,
        btc=f"<code>{wallets.btc}</code>" if wallets and wallets.btc else 'Не привязан',
        eth=f"<code>{wallets.eth}</code>" if wallets and wallets.eth else 'Не привязан',
        trc20=f"<code>{wallets.trc20}</code>" if wallets and wallets.trc20 else 'Не привязан',
        tron=f"<code>{wallets.trx}</code>" if wallets and wallets.trx else 'Не привязан'
    ), reply_markup=kb.profile_kb(), parse_mode='HTML')


@router.callback_query(F.data == callbacks['🆙 Повысить лимиты'])
async def profile_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(LEXICON_RU['dev'])


@router.callback_query(F.data == callbacks['📝 Изменить информацию'])
async def profile_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(LEXICON_RU['dev'])


@router.callback_query(F.data == callbacks[buttons['link_wallet']])
async def profile_menu(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON_RU['choose_wallet'], reply_markup=kb.wallets())


@router.callback_query(F.data.startswith('wallet'))
async def enter_wallet(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    wallet = callback.data.split('_')[1]
    await callback.message.edit_text(LEXICON_RU['enter_wallet'].format(wallet.upper()))
    await state.set_state(UserState.enter_wallet)
    await state.update_data({'wallet': wallet})


@router.message(StateFilter(UserState.enter_wallet))
async def enter_wallet(message: Message, state: FSMContext):
    data = await state.get_data()
    if await db.wallet_exists(message.from_user.id):
        await db.add_wallet(message.from_user.id, {data['wallet']: message.text})
    else:
        await db.set_wallet(message.from_user.id)
        await db.add_wallet(message.from_user.id, {data['wallet']: message.text})
    await message.answer(f"кошелёк {data['wallet'].upper()} установлен")
    await state.clear()


@router.callback_query(F.data == callbacks['💸 Запросить выплату'])
async def choose_wallet_for_payout(callback: CallbackQuery):
    await callback.answer()
    user = await db.get_user(callback.from_user.id)
    linked_wallets = await db.get_linked_wallets(callback.from_user.id)

    if not user:
        await db.set_wallet(callback.from_user.id)
    if not user.balance:
        await callback.message.answer(LEXICON_RU['no_money'])
        if callback.from_user.id in config.tg_bot.admin_ids:
            await callback.message.answer('Поскольку Вы являетесь администратором, в целях тестирования Вам доступна'
                                          'команда <code>/add n</code> для зачисления на баланс n денег',
                                          parse_mode='HTML')
    elif linked_wallets:
        await callback.message.edit_text(LEXICON_RU['choose_wallet_for_payout'],
                                         reply_markup=kb.walets_for_payout(linked_wallets))
    else:
        await callback.message.answer(LEXICON_RU['no_wallets'])
        await callback.answer()


@router.callback_query(F.data.startswith('payout'))
async def enter_payout_amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user = await db.get_user(callback.from_user.id)
    mes = await callback.message.edit_text(
        LEXICON_RU['payout_amount'].format(balance=str(user.balance)),
        reply_markup=kb.back(),
        parse_mode='HTML')
    await state.set_state(UserState.enter_payout_amount)
    await state.update_data({"wallet_type": callback.data.split('_')[1], "message": mes, "new_mes": None})


@router.callback_query(F.data == callbacks['⭐️ Установить никнейм'])
async def enter_nickname(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['enter_nickname'], reply_markup=kb.back())
    await state.set_state(UserState.enter_nickname)


@router.message(StateFilter(UserState.enter_nickname))
async def set_nickname(message: Message, state: FSMContext):
    try:
        await db.set_nickname(message.from_user.id, message.text)
        await message.answer(LEXICON_RU['nickname_is_set'].format(message.text))
    except Exception as e:
        await message.answer(str(e))
    await state.clear()
