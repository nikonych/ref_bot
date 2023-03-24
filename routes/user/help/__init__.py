from aiogram import Router
from aiogram.filters import CommandStart, Text

from utils.misc.kb_config import help_btn
from .help import help_handler

help_router = Router()

help_router.message.register(help_handler, Text(text=help_btn))

