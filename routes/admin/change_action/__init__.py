from aiogram import Router, F
from aiogram.filters import Text, StateFilter

from misc.states import ChangeState
from utils.misc.kb_config import change_action_btn
from .change_action import change_description, change_handler, change_name, change_price, get_name, get_description, \
    get_price

change_action_router = Router()
change_action_router.message.register(change_handler, Text(startswith=change_action_btn))
change_action_router.callback_query.register(change_name, Text(startswith="change_action_name"))
change_action_router.callback_query.register(change_description, Text(startswith="change_action_description"))
change_action_router.callback_query.register(change_price, Text(startswith="change_action_price"))
change_action_router.message.register(get_name, StateFilter(ChangeState.new_action_name))
change_action_router.message.register(get_description, StateFilter(ChangeState.new_action_description))
change_action_router.message.register(get_price, StateFilter(ChangeState.new_action_price))