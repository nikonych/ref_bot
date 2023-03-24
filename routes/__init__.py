from aiogram import Dispatcher, Router, F

from config import Config
from . import global_filter
from . import pagination
from .admin import admin_router
from .chat import chat_router
# from .admin import admin_router
from .errors import errors_router
from .user import user_router
from .user.tokens import tokens_router


def register_all_routes(dp: Dispatcher, config: Config):
    master_router = Router()

    # master_router.callback_query.register(pagination.pagination_handler, text_startswith=('next:', 'prev:'))
    # master_router.message.register(global_filter.dev_handler, commands='dev')

    dp.include_router(master_router)
    dp.include_router(errors_router)

    admin_router.message.filter(F.from_user.id.in_(config.tg_bot.admin_ids))
    user_router.message.filter(F.chat.id > 0)
    admin_router.message.filter(F.chat.id > 0)

    master_router.include_router(user_router)
    master_router.include_router(chat_router)
    master_router.include_router(admin_router)
    # master_router.include_router(admin_router)
