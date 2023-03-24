from aiogram import Router, F
from aiogram.filters import Text, StateFilter

from misc.states import ChangeState
from utils.misc.kb_config import change_desc_btn
from .change_text import change_text, get_text

change_text_router = Router()
change_text_router.callback_query.register(change_text, Text(startswith="change_text:"))
change_text_router.message.register(get_text, StateFilter(ChangeState.new_text))