from aiogram import Router
from aiogram.filters import CommandStart, Text

from utils.misc.kb_config import  information_btn
from .information import information_handler

information_router = Router()

information_router.message.register(information_handler, Text(text=information_btn))

