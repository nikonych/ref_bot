from aiogram import Router
from aiogram.filters import Text

from routes.user.action.action import get_actions_type_handler, get_action_detail_handler, buy_action_handler, \
    chose_refill_type_handler, get_refill_count_handler, check_pay_handler
from utils.misc.kb_config import action_btn

action_router = Router()

action_router.message.register(get_actions_type_handler, Text(text=action_btn))
action_router.callback_query.register(chose_refill_type_handler, Text(startswith="pay_action"))
action_router.callback_query.register(get_refill_count_handler, Text(startswith="refill_type:"))
action_router.callback_query.register(check_pay_handler, Text(startswith="check_pay:"))