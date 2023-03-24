import json
import pyqiwi
from aiogram.types import CallbackQuery
from pyqiwi.exceptions import APIError

async def check_qiwi(call: CallbackQuery):
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    try:
        wallet = pyqiwi.Wallet(token=data['payments']['qiwi_token'])
        await call.message.answer("QIWI успешно работает!\n"
                                  f"На балансе: {wallet.balance()}₽")
    except APIError:
        await call.answer("Неверный токен")

async def auto_withdraw(recipient, amount, call: CallbackQuery):
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    try:
        print(recipient, amount)
        wallet = pyqiwi.Wallet(token=data['payments']['qiwi_token'])
        pay = wallet.send(pid='99', recipient=recipient, amount=amount, comment="Спасибо что работаете с нами!")
        print(pay)
        print(pay.transaction['state']['code'])
    except APIError:
        await call.answer("Неверный токен! Измените в админке")
