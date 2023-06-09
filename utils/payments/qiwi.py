import asyncio
import json
import random
import secrets
import time

import pyqiwi
from aiogram.types import CallbackQuery
from async_class import AsyncClass
from pyqiwi.exceptions import APIError
from pyqiwip2p import QiwiP2P


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


class QiwiAPI(AsyncClass):
    async def __ainit__(self):
        settings = open("database/settings.json", "r")
        with settings as read_file:
            data = json.load(read_file)
        self.token = data['payments']['qiwi_token']

        self.base_url = "https://edge.qiwi.com/{}/{}/persons/{}/{}"
        self.headers = {"authorization": f"Bearer {self.token}"}

    # Создание платежа
    async def bill_pay(self, get_amount):
        receipt = self.get_random_string()
        settings = open("database/settings.json", "r")
        with settings as read_file:
            data = json.load(read_file)
        token = data['payments']['qiwi_secret']
        qiwi = QiwiP2P(token)
        bill = qiwi.bill(bill_id=receipt, amount=get_amount, comment=receipt)
        send_requests = bill.pay_url

        return_message = f"<b>🆙 Пополнение баланса</b>\n" \
                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                         f"🥝 Для пополнения баланса, нажмите на кнопку ниже \n<code>Перейти к оплате</code> и оплатите выставленный вам счёт\n" \
                         f"❗ У вас имеется 30 минут на оплату счета.\n" \
                         f"💰 Сумма пополнения: <code>{get_amount}₽</code>\n" \
                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                         f"🔄 После оплаты, нажмите на <code>Проверить оплату</code>"

        return return_message, send_requests, receipt

    def get_random_string(self):
        return f'{time.time()}_{secrets.token_hex(random.randint(12, 20))}'

    # Проверка платежа по форме
    async def check_form(self, receipt):
        settings = open("database/settings.json", "r")
        with settings as read_file:
            data = json.load(read_file)
        token = data['payments']['qiwi_secret']
        qiwi_p2p = QiwiP2P(token)
        get_pay = qiwi_p2p.check(bill_id=receipt)

        pay_status = get_pay.status  # Получение статуса платежа
        pay_amount = int(float(get_pay.amount))  # Получение суммы платежа в рублях

        return pay_status, pay_amount

# Проверка платежа по переводу
