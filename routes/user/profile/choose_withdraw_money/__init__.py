from aiogram import Router
from aiogram.filters import Text

from .choose_withdraw import choose_withdraw_handler

choose_withdraw_router = Router()

choose_withdraw_router.callback_query.register(choose_withdraw_handler, Text(startswith="withdraw_money"))