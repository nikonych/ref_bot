from aiogram import Router, F
from aiogram.filters import Text, StateFilter

from misc.states import ChangeState
from utils.misc.kb_config import change_desc_btn
from .change_img import change_img, get_img

change_img_router = Router()
change_img_router.callback_query .register(change_img, Text(startswith="change_img:"))
change_img_router.message.register(get_img, StateFilter(ChangeState.new_img))