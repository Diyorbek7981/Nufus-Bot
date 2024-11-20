from aiogram.fsm.state import StatesGroup, State


class SignupStates(StatesGroup):
    name = State()
    gender = State()
    age = State()
    phone = State()
    verify = State()
    feedback = State()
    rate = State()
    verify_fb = State()
