from aiogram import Router
from aiogram.filters import Text

from misc.states import TokenState
from .ask_proof import ask_proof_handler

ask_proof_router = Router()

ask_proof_router.callback_query.register(ask_proof_handler, Text(startswith='send_proof:'))