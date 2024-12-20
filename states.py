from aiogram.fsm.state import StatesGroup, State


class SignupStates(StatesGroup):
    name = State()
    age = State()
    phone = State()
    verify = State()
    feedback = State()
    items = State()
