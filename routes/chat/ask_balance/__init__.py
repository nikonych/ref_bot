from aiogram import Router
from aiogram.filters import Text

from misc.states import TokenState
from routes.chat.ask_balance.ask_balance import ask_balance_handler

ask_balance_router = Router()

ask_balance_router.callback_query.register(ask_balance_handler, Text(startswith='add_money:'))