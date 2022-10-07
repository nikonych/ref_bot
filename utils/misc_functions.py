# - *- coding: utf- 8 - *-
import asyncio
from datetime import datetime

import requests
from aiogram import Dispatcher
from bs4 import BeautifulSoup




# Рассылка сообщения всем администраторам
# async def send_admins(message, markup=None, not_me=0):
#     for admin in get_admins():
#         if markup == "default":
#             markup = menu_frep(admin)
#
#         try:
#             if str(admin) != str(not_me):
#                 await bot.send_message(admin, message, reply_markup=markup, disable_web_page_preview=True)
#         except:
#             pass


# Автоматическая очистка ежедневной статистики после 00:00
# async def update_logs_day():
#     print("day_start")
#     update_logs(daylogs=0, daycolds=0)
#
# async def update_logs_week():
#     update_logs(weeklogs=0, weekcolds=0)
#
# async def update_logs_month():
#     update_logs(monthlogs=0, monthcolds=0)

