import json
import time

import requests
from aiogram.types import CallbackQuery
from .lolzapi import LolzteamApi


async def check_lzt(call: CallbackQuery):
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    api = LolzteamApi(data['payments']['lzt_token'])
    me = api.market_me()
    if not ("error" in list(me.keys())):
        await call.message.answer("LZT успешно работает!\n"
                                  f"На балансе: {me['user']['balance']}₽")
        return me['user']['balance']
    else:
        await call.answer("Неверный токен")


async def get_balance():
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    api = LolzteamApi(data['payments']['lzt_token'])
    me = api.market_me()
    if not ("error" in list(me.keys())):
        time.sleep(3)
        return me['user']['balance']
    return None


async def auto_withdraw(user_id, user_name, amount, call: CallbackQuery):
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    api = LolzteamApi(data['payments']['lzt_token'])
    me = api.market_me()
    if not ("error" in list(me.keys())):
        time.sleep(3)
        pay = api.market_transfer(receiver=user_id, receiver_username=user_name, amount=amount,
                                  secret_answer=data['payments']['lzt_secret'], comment="Спасибо что работаете с нами!")
        if pay.status_code == 200:
            await call.message.edit_text(call.message.text + "\n\n"
                                                             "Выплачено", reply_markup=None)
            return True
    else:
        await call.answer("Неверный токен! Измените в админке")
    return False
