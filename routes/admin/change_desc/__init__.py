from aiogram import Router, F
from aiogram.filters import Text

from utils.misc.kb_config import change_desc_btn
from .change_desc import change_desc_handler
change_desc_router = Router()
change_desc_router.message.register(change_desc_handler, Text(startswith=change_desc_btn))