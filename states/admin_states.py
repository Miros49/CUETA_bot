from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    enter_event_name: State = State()
    enter_event_description: State = State()
    enter_event_date: State = State()
