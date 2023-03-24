from aiogram import Router, F
from aiogram.filters import StateFilter
from misc.states import TokenState
from .get_proof import get_proof_album_handler

get_proof_router = Router()

get_proof_router.message.register(get_proof_album_handler, StateFilter(TokenState.proof))
# get_proof_router.message.register(get_proof_handler, StateFilter(TokenState.proof), F.photo)