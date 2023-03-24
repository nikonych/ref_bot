from aiogram import Router
from aiogram.filters import Text

from . import upload_file



upload_router = Router()

upload_router.callback_query.register(upload_file.upload_handler, Text(startswith="send_txt:"))