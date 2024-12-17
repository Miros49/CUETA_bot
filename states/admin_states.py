from aiogram.fsm.state import State, StatesGroup, default_state


class AdminState(StatesGroup):
    default_state: State = default_state
    enter_event_name: State = State()
    enter_event_description: State = State()
    enter_event_date: State = State()
