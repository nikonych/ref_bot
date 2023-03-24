from aiogram import Router, F
from aiogram.filters import Text, StateFilter

from misc.states import UserState
from routes.admin.users.users import users_handler, get_user_handler, find_user_handler, users_list_handler, \
    select_user_handler
from utils.misc.kb_config import statistic_btn, users_btn

users_router = Router()
users_router.message.register(users_handler, Text(text=users_btn))
users_router.callback_query.register(find_user_handler, Text(text="find_user"))
users_router.callback_query.register(users_list_handler, Text(startswith="users_list"))
users_router.callback_query.register(select_user_handler, Text(startswith="show_user_detail:"))
users_router.message.register(get_user_handler, StateFilter(UserState.user_id))
