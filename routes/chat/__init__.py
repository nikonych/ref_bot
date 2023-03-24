from aiogram import Router
from aiogram.filters import CommandStart

from .add_balance import add_balance_router
from .ask_balance import ask_balance_router
from .ask_proof import ask_proof_router
from .empty_token import empty_token_router
from .get_proof import get_proof_router
from .sure_empty import sure_empty_router
from .withdraw import withdraw_router

# from

chat_router = Router()
# user_router.callback_query.register(start.back_to_start_handler)
# # user_router.callback_query.register(start.back_to_start_handler, text='back_in_menu')
# user_router.message.register(start.start_handler)
# user_router.message.register(start.start_handler, text='⬅️ Вернуться в меню')
# user_router.message.register(empty_token.start_handler)

chat_router.include_router(empty_token_router)
chat_router.include_router(sure_empty_router)
chat_router.include_router(ask_balance_router)
chat_router.include_router(add_balance_router)
chat_router.include_router(ask_proof_router)
chat_router.include_router(get_proof_router)
chat_router.include_router(withdraw_router)
# user_router.include_router(profile_router)
# user_router.include_router(tokens_router)
