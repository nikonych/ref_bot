from aiogram import Router
from aiogram.filters import Text, StateFilter

from misc.states import WithdrawState
from .ask_withdraw import ask_withdraw_handler
from .ask_withdraw_link import ask_withdraw_link_handler, ask_withdraw_user_name_handler
from .ask_withdraw_money import ask_withdraw_money_handler
from .ask_withdraw_number import ask_withdraw_number_handler

ask_withdraw_router = Router()

ask_withdraw_router.callback_query.register(ask_withdraw_handler, Text(startswith="choose_withdraw:"))
ask_withdraw_router.message.register(ask_withdraw_number_handler, StateFilter(WithdrawState.number))
ask_withdraw_router.message.register(ask_withdraw_link_handler, StateFilter(WithdrawState.link))
ask_withdraw_router.message.register(ask_withdraw_user_name_handler, StateFilter(WithdrawState.user_name))
ask_withdraw_router.message.register(ask_withdraw_money_handler, StateFilter(WithdrawState.money))