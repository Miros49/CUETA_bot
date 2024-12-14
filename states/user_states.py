from aiogram.fsm.state import default_state, State, StatesGroup


class UserState(StatesGroup):
    create_profile_1: State = State()
    create_profile_2: State = State()
    create_profile_3: State = State()
    create_profile_4: State = State()
    create_profile_5: State = State()
    create_profile_6: State = State()
    create_profile_7: State = State()
    choose_wallet: State = State()
    enter_nickname: State = State()
    checker_enter_link: State = State()
    enter_wallet: State = State()
    enter_promo: State = State()
    generators: State = State()
    generate_tags: State = State()
    enter_payout_amount: State = State()
    create_promo_amount: State = State()
    create_promo_custom: State = State()
    enter_creo_domain: State = State()
    enter_creo_promo: State = State()
    enter_creo_amount: State = State()
