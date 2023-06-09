from aiogram import Router, F
from aiogram.filters import Text

from utils.misc.kb_config import admin_btn, back_btn
from .admin import admin_menu_handler
from .change_action import change_action_router
from .change_desc import change_desc_router
from .change_img import change_img_router
from .change_text import change_text_router
from .change_url import change_url_router
from .payments import payments_router
from .statistic import statistics_router
from .users import users_router
from ..user.start import back_to_start_handler

admin_router = Router()
admin_router.message.register(admin_menu_handler, Text(startswith=admin_btn))
admin_router.message.register(back_to_start_handler, Text(startswith=back_btn))

admin_router.include_router(change_desc_router)
admin_router.include_router(change_img_router)
admin_router.include_router(change_text_router)
admin_router.include_router(change_url_router)
admin_router.include_router(statistics_router)
admin_router.include_router(users_router)
admin_router.include_router(payments_router)
admin_router.include_router(change_action_router)