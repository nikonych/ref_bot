from aiogram import Router
from aiogram.filters import Text, StateFilter

from misc.states import TokenState
from . import empty_token

empty_token_router = Router()

empty_token_router.callback_query.register(empty_token.empty_token_handler, Text(startswith='empty:'))
