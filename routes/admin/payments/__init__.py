from aiogram import Router, F
from aiogram.filters import Text, StateFilter

from misc.states import UserState, PaymentState
from routes.admin.payments.change_payments import change_payment_handler, get_token_handler, get_secret_handler, \
    get_wallet_handler
from routes.admin.payments.check_payments import check_payment_handler
from routes.admin.payments.payments import payments_handler
from utils.misc.kb_config import payments_btn

payments_router = Router()
payments_router.message.register(payments_handler, Text(text=payments_btn))
payments_router.callback_query.register(change_payment_handler, Text(startswith="change_payment:"))
payments_router.callback_query.register(check_payment_handler, Text(startswith="check_payment:"))
payments_router.message.register(get_token_handler, StateFilter(PaymentState.token))
payments_router.message.register(get_secret_handler, StateFilter(PaymentState.secret))
payments_router.message.register(get_wallet_handler, StateFilter(PaymentState.wallet))
