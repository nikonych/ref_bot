from aiogram import Router, F
from aiogram.filters import Text, StateFilter

from misc.states import ChangeState
from utils.misc.kb_config import change_desc_btn
from .change_url import change_url, get_url

change_url_router = Router()
change_url_router.callback_query.register(change_url, Text(startswith="change_url:"))
change_url_router.message.register(get_url, StateFilter(ChangeState.new_url))