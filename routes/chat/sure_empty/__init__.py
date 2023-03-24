from aiogram import Router
from aiogram.filters import Text

from .sure_empty import sure_empty_handler

sure_empty_router = Router()

sure_empty_router.callback_query.register(sure_empty_handler, Text(startswith="sure:"))
