from aiogram import Router
from aiogram.filters import CommandStart, Text

from . import start
from .about_us import about_us_router
from .action import action_router
from .help import help_router
from .information import information_router
# from .about import about_router
from .profile import profile_router


# from .purchase import purchase_router

user_router = Router()
# user_router.callback_query.register(start.back_to_start_handler)
# # user_router.callback_query.register(start.back_to_start_handler, text='back_in_menu')
# user_router.message.register(start.start_handler)
# user_router.message.register(start.start_handler, text='⬅️ Вернуться в меню')
user_router.message.register(start.start_handler, CommandStart())
user_router.callback_query.register(start.accept_license_handler, Text(text='accept_license'))

# user_router.include_router(purchase_router)
user_router.include_router(profile_router)
user_router.include_router(help_router)
user_router.include_router(information_router)
user_router.include_router(about_us_router)
user_router.include_router(action_router)
