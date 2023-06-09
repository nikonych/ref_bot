import json
import random
import secrets
import time



from aiogram.types import CallbackQuery

from utils.payments.LavaAPI import Payment, LavaAPI


def get_random_string():
    return f'{time.time()}_{secrets.token_hex(random.randint(12, 20))}'


async def bill_pay(get_amount):
    receipt = get_random_string()
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    api = LavaAPI(data['payments']['lava_token'])
    print(api.__dict__)
    bill = api.create_invoice(get_amount, receipt)

    return_message = f"<b>🆙 Пополнение баланса</b>\n" \
                     f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                     f"🥝 Для пополнения баланса, нажмите на кнопку ниже \n<code>Перейти к оплате</code> и оплатите выставленный вам счёт\n" \
                     f"❗ У вас имеется 30 минут на оплату счета.\n" \
                     f"💰 Сумма пополнения: <code>{get_amount}₽</code>\n" \
                     f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                     f"🔄 После оплаты, нажмите на <code>Проверить оплату</code>"

    return return_message, bill, receipt


async def check_form(payment: Payment):
    return payment.is_paid(), payment.amount


async def check_lava(call: CallbackQuery):
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    api = LavaAPI(data['payments']['lava_token'])

    if api.check_key():
        await call.message.answer("LAVA успешно работает!\n"
                                  f"На балансе: {api.wallet_balance('RUB')}₽")
        return api.wallet_balance("RUB")
    else:
        await call.answer("Неверный токен")
