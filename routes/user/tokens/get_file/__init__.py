from aiogram import Router, F
from aiogram.filters import Text, StateFilter

from misc.states import TokenState
from . import get_file



get_file_router = Router()

get_file_router.message.register(get_file.get_file_handler, StateFilter(TokenState.file), F.document)