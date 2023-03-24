from aiogram.fsm.state import StatesGroup, State


class TokenState(StatesGroup):
    file = State()
    money = State()
    proof = State()


class WithdrawState(StatesGroup):
    number = State()
    link = State()
    user_name = State()
    money = State()

class ChangeState(StatesGroup):
    new_img = State()
    new_text = State()
    new_url = State()

class UserState(StatesGroup):
    user_id = State()

class PaymentState(StatesGroup):
    token = State()
    number = State()
    secret = State()