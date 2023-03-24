from aiogram import Router
from aiogram.enums import ContentType
from aiogram.filters import Text

from utils.misc.kb_config import load_token_btn
from . import tokens
from .upload_file import upload_router
from .get_file import get_file_router

tokens_router = Router()

tokens_router.message.register(tokens.tokens_handler, Text(text=load_token_btn))
tokens_router.include_router(upload_router)
tokens_router.include_router(get_file_router)