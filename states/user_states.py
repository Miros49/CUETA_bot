from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    sign_in_enter_name: State = State()
    sign_in_enter_date_of_birth: State = State()
    sign_in_enter_status: State = State()
    sign_in_enter_phone_number: State = State()
