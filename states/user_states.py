from aiogram.fsm.state import State, StatesGroup, default_state


class UserState(StatesGroup):
    default_state: State = default_state
    sign_in_enter_name: State = State()
    sign_in_enter_date_of_birth: State = State()
    sign_in_enter_status: State = State()
    sign_in_enter_phone_number: State = State()

    send_payment_confirmation: State = State()

    enter_coins_amount: State = State()
