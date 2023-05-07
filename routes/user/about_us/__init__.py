from aiogram import Router
from aiogram.filters import Text

from utils.misc.kb_config import about_us_btn
from .about_us import about_us_handler

about_us_router = Router()

about_us_router.message.register(about_us_handler, Text(text=about_us_btn))

