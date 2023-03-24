import json
from yoomoney import Client
from aiogram.types import CallbackQuery
from yoomoney.exceptions import InvalidToken
async def check_yoomoney(call: CallbackQuery):
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    try:
        client = Client(data['payments']['yoomoney_token'])
        user = client.account_info()
        await call.message.answer("YooMoney успешно работает!\n"
                                  f"На балансе: {user.balance}₽")
    except InvalidToken:
        await call.answer("Неверный токен")

