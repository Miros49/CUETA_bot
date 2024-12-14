from aiogram.fsm.state import default_state, State, StatesGroup


class AdminState(StatesGroup):
    enter_message: State = State()
    enter_admin_id: State = State()
    ban_user: State = State()
