from aiogram import Router, F
from aiogram.filters import Text

from routes.admin.statistic.stats import statistics_handler
from utils.misc.kb_config import statistic_btn

statistics_router = Router()
statistics_router.message.register(statistics_handler, Text(text=statistic_btn))