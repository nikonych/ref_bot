import json
import random
import secrets
import time

import requests
from aiogram.types import CallbackQuery
from async_class import AsyncClass

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
                                                             "✅ Выплачено", reply_markup=None)
            return True
    else:
        await call.answer("Неверный токен! Измените в админке")
    return False


class Lolz(AsyncClass):
    async def __ainit__(self):
        self.api_url = 'https://api.zelenka.guru/'
        settings = open("database/settings.json", "r")
        with settings as read_file:
            data = json.load(read_file)
        self.access_token = data['payments']['lzt_token']
        self.user_id = data['payments']['lzt_id']

        self.session = requests.session()
        self.session.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        self.user = self.get_user()
        if self.user != None:
            self.username = self.user['username']
            self.balance = self.user['balance']



    def get_user(self):
        print(self.session.headers)
        response = self.session.get('https://api.zelenka.guru/market/me')
        if response.status_code == 200:
            response = response.json()
            if 'user' not in response.keys():
                raise ValueError('Invalid Token')
            return response['user']
        else:
            pass

    async def get_link(self, amount: int, comment: str):
        return_message = f"<b>💳 Пополнение баланса на сумму {amount}₽</b>\n" \
                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                         f"1️⃣  Для пополнения баланса, нажмите на кнопку ниже " \
                         "<code>Оплатить</code> и оплатите выставленный вам счёт\n" \
                         "2️⃣ После оплаты, нажмите на <code>Проверить оплату</code>\n"
        payment = f'https://lolz.guru/market/balance/transfer?username={self.username}&hold=0&amount={amount}&comment={comment}'

        return payment, return_message
        # return f'https://lolz.guru/market/balance/transfer?username={self.username}&hold=0&amount={amount}&comment={comment}'

    def get_random_string(self):
        return f'{time.time()}_{secrets.token_hex(random.randint(12, 20))}'

    def check_payment(self, amount: int, comment: str):
        data = {
            "type": "money_transfer",
            "is_hold": 0
        }
        session = requests.session()
        session.headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        response = session.get(f'{self.api_url}market/user/{self.user_id}/payments')
        print(response)
        if response.status_code == 200:
            payments = response.json()['payments']
            for payment in payments.values():
                if 'Перевод денег от' in payment['label']['title'] and int(amount) == payment[
                    'incoming_sum'] and comment == payment['data']['comment']:
                    return True
            return False
        else:
            pass



