from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import Text

from utils.misc.kb_config import profile_btn
from . import profile
from .ask_withdraw import ask_withdraw_router
from .choose_withdraw_money import choose_withdraw_router

profile_router = Router()

profile_router.message.register(profile.profile_handler, Text(text=profile_btn))
profile_router.callback_query.register(profile.profile_handler, Text(text='back_profile'))

profile_router.include_router(choose_withdraw_router)
profile_router.include_router(ask_withdraw_router)


