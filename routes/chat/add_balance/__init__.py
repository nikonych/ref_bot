from aiogram import Router, F
from aiogram.filters import Text, StateFilter

from misc.states import TokenState
from routes.chat.add_balance.add_balance import add_balance_handler

add_balance_router = Router()

add_balance_router.message.register(add_balance_handler, StateFilter(TokenState.money))