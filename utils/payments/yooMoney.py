import json
import random
import secrets
import string
import time

import requests
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from async_class import AsyncClass
from os import path

from yoomoney import Client, Quickpay


async def check_yoomoney(call: CallbackQuery):
    try:
        settings = open("database/settings.json", "r")
        with settings as read_file:
            data = json.load(read_file)
        client = Client(data['payments']['yoo_token'])
        user = client.account_info()
        await call.message.answer(f"<b>YooMoney полностью функционирует</b>\n"
                                  f"◾ Wallet: <code>{user.account}</code>\n"
                                  f"◾ Токен: <code>{data['payments']['yoo_token']}</code>\n")
    except:
        await call.answer("Неверный токен")


class YooMoneyAPI(AsyncClass):
    async def __ainit__(self):
        self.scope= ["account-info",
                               "operation-history",
                               "operation-details",
                               "incoming-transfers",
                               "payment-p2p",
                               "payment-shop",
                               ]

    def get_random_string(self):
        return f'{time.time()}_{secrets.token_hex(random.randint(5, 10))}'

    # Создание платежа
    async def bill_pay(self, get_amount):
        receipt = self.get_random_string()
        settings = open("database/settings.json", "r")
        with settings as read_file:
            data = json.load(read_file)
        wallet = data['payments']['yoo_wallet']
        quickpay = Quickpay(
            receiver=wallet,
            quickpay_form="shop",
            targets="gg",
            paymentType="SB",
            sum=get_amount,
            label=receipt
        )

        return_message = f"<b>💳 Пополнение баланса на сумму {get_amount}₽</b>\n" \
                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                             f"1️⃣  Для пополнения баланса, нажмите на кнопку ниже "\
                                    "<code>Оплатить</code> и оплатите выставленный вам счёт\n" \
                                    "2️⃣ После оплаты, нажмите на <code>Проверить оплату</code>\n"
        return return_message, quickpay.base_url, receipt


    async def check_pay(self, label):
        settings = open("database/settings.json", "r")
        with settings as read_file:
            data = json.load(read_file)
        client = Client(data['payments']['yoo_token'])
        history = client.operation_history(label=label)
        for operation in history.operations:
            # print()
            # print("Operation:", operation.operation_id)
            # print("\tStatus     -->", operation.status)
            # print("\tDatetime   -->", operation.datetime)
            # print("\tTitle      -->", operation.title)
            # print("\tPattern id -->", operation.pattern_id)
            # print("\tDirection  -->", operation.direction)
            # print("\tAmount     -->", operation.amount)
            # print("\tLabel      -->", operation.label)
            # print("\tType       -->", operation.type)
            return True, operation.amount
        return False, None



    # async def get_link(self):
    #     self.url = "https://yoomoney.ru/oauth/authorize?client_id={client_id}&response_type=code" \
    #                "&redirect_uri={redirect_uri}&scope={scope}".format(client_id=self.client_id,
    #                                                                    redirect_uri=self.redirect,
    #                                                                    scope='%20'.join(
    #                                                                        [str(elem) for elem in self.scope]),
    #                                                                    )
    #
    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #
    #     response = requests.request("POST", self.url, headers=headers)
    #
    #     if response.status_code == 200:
    #         return response.url
    #         keyboard = InlineKeyboardMarkup()
    #         keyboard.add(InlineKeyboardButton("Ссылка на авторизацию", url=response.url))
    #         await self.dp.answer("<b>1) Посетите этот веб-сайт</b> \n"
    #                              "<b>2) Подтвердите запрос на авторизацию приложения</b>\n"
    #                              "<b>3) После подтверждения отправьте ссылку сайта на который вас перенесли</b>",
    #                              reply_markup=keyboard)
    #     return False


    # async def get_token(self, link):
    #     try:
    #         code = link[link.index("code=") + 5:].replace(" ","")
    #
    #     except:
    #         pass
    #
    #     url = "https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&" \
    #           "grant_type=authorization_code&redirect_uri={redirect_uri}".format(code=str(code),
    #                                                                              client_id=self.client_id,
    #                                                                              redirect_uri=self.redirect,
    #                                                                              )
    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #
    #     self.response = requests.request("POST", url, headers=headers)
    #     if "error" in self.response.json():
    #         return False
    #     if self.response.json()['access_token'] == "":
    #         return False
    #
    #
    #     return self.response.json()['access_token']





    async def get_balance(self):
        try:
            client = Client(self.token)
            user = client.account_info()
            await self.dp.answer(f"<b>🌍 Баланс кошелька <code>{user.account}</code> составляет:</b>\n"
                                 f"🇷🇺 Рублей: <code>{user.balance}₽</code>")
        except:
            await self.error_wallet()
            return False
