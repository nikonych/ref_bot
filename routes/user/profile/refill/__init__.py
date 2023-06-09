
from aiogram import Router
from aiogram.filters import Text, StateFilter

from misc.states import UserState
# from routes.user.profile.refill.refill import chose_refill_type_handler, ask_refill_count_handler, \
#     get_refill_count_handler, check_pay_handler

refill_router = Router()

# refill_router.callback_query.register(chose_refill_type_handler, Text(startswith="refill_money"))
# refill_router.callback_query.register(ask_refill_count_handler, Text(startswith="refill_type:"))
# refill_router.message.register(get_refill_count_handler, StateFilter(UserState.refill_count))
# refill_router.callback_query.register(check_pay_handler, Text(startswith="check_pay:"))