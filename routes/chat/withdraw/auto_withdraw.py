import requests
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from requests.utils import default_headers
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from utils.misc.kb_config import qiwi_btn, lolz_btn, yoomoney_btn, bank_card_btn, back_btn
from utils.payments import qiwi, lzt
from utils.payments.lzt import check_lzt, get_balance


async def auto_withdraw_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    user_id = int(call.data.split(":")[1])
    type = call.data.split(":")[2]
    link = call.data.split(":")[3]
    money = call.data.split(":")[4]


    if type == "QIWI":
        balance = await get_balance()
        if balance:
            if balance >= int(call.data.split(":")[5]):
                result = await qiwi.auto_withdraw(recipient=link, amount=int(money), call=call)
                if result:
                    money = int(call.data.split(":")[5])
                    user_db = await DBCommands(User, session).get(user_id=user_id)
                    await DBCommands(User, session).update(values=dict(wait_balance=user_db.wait_balance - int(money),
                                                                       withdraw_balance=user_db.withdraw_balance + int(
                                                                           money)), where=dict(user_id=user_id))

                    await bot.send_message(chat_id=user_id, text="✅ Ваша заявка на вывод средств успешно выполнена!")
            else:
                await call.answer("Недостаточно средств!\n"
                                  f"На балансе: {balance}₽")
    elif type == 'LOLZ':
        balance = await get_balance()
        if balance:
            if balance >= int(call.data.split(":")[5]):
                result = await lzt.auto_withdraw(user_id=link, user_name=call.data.split(":")[4], amount=int(call.data.split(":")[5]), call=call)
                if result:
                    money = int(call.data.split(":")[5])
                    user_db = await DBCommands(User, session).get(user_id=user_id)
                    await DBCommands(User, session).update(values=dict(wait_balance=user_db.wait_balance - int(money),
                                                                       withdraw_balance=user_db.withdraw_balance + int(
                                                                           money)), where=dict(user_id=user_id))

                    await bot.send_message(chat_id=user_id, text="✅ Ваша заявка на вывод средств успешно выполнена!")
            else:
                await call.answer("Недостаточно средств!\n"
                                  f"На балансе: {balance}₽")
        # headers = default_headers()
        #
        # headers.update(
        #     {
        #         'User-Agent': 'My User Agent 1.0',
        #     }
        # )
        #
        # response = requests.get("https://lolz.guru/members/1", headers=headers)
        # print(response.headers)
    # user_db = await DBCommands(User, session).get(user_id=user_id)
    # await DBCommands(User, session).update(values=dict(wait_balance=user_db.wait_balance-int(money), withdraw_balance=user_db.withdraw_balance + int(money)), where=dict(user_id=user_id))
    #
    # await bot.send_message(chat_id=user_id, text="Ваша заявка на вывод средств успешно выполнена!")
    #
    # await call.message.edit_text(call.message.text + "\n"
    #                                                  "Выплачено автовыводом", reply_markup=None)

