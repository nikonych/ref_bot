from aiogram import Router
from aiogram.filters import Text

from .auto_withdraw import auto_withdraw_handler
from .error_number_withdraw import error_number_withdraw_handler
from .had_withdraw import had_withdraw_handler

withdraw_router = Router()

withdraw_router.callback_query.register(error_number_withdraw_handler, Text(startswith="error_number:"))
withdraw_router.callback_query.register(had_withdraw_handler, Text(startswith="had_withdraw:"))
withdraw_router.callback_query.register(auto_withdraw_handler, Text(startswith="auto_withdraw:"))