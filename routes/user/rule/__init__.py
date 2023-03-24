from aiogram import Router
from aiogram.filters import CommandStart, Text

from utils.misc.kb_config import help_btn, rule_btn
from .rule import rule_handler

rule_router = Router()

rule_router.message.register(rule_handler, Text(text=rule_btn))

