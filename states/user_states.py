<<<<<<< HEAD
from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
=======
from aiogram.fsm.state import State, StatesGroup, default_state


class UserState(StatesGroup):
    default_state: State = default_state
>>>>>>> miros
    sign_in_enter_name: State = State()
    sign_in_enter_date_of_birth: State = State()
    sign_in_enter_status: State = State()
    sign_in_enter_phone_number: State = State()
