import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from database.models.withdraw import Withdraw
from utils.misc.kb_config import qiwi_btn, lolz_btn, yoomoney_btn, bank_card_btn, back_btn


async def had_withdraw_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    user_id = int(call.data.split(":")[1])
    money = int(call.data.split(":")[2])
    withdraw_id = call.data.split(":")[3]
    await call.message.edit_text(call.message.text + "\n"
                                                     "✅ Выплачено", reply_markup=None)

    user_db = await DBCommands(User, session).get(user_id=user_id)
    await DBCommands(User, session).update(values=dict(wait_balance=user_db.wait_balance-int(money), withdraw_balance=user_db.withdraw_balance + int(money)), where=dict(user_id=user_id))
    await DBCommands(Withdraw, session).update(values=dict(withdraw_status="Выплачено"), where=dict(withdraw_id=withdraw_id))
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    withdraw_chat_id = data['withdraw_chat_id']
    withdraw_db = await DBCommands(Withdraw, session).get(withdraw_id=withdraw_id)
    formatted_date = withdraw_db.withdraw_date.strftime('%d.%m.%Y')
    await bot.send_message(chat_id=int(withdraw_chat_id), text="🔗 Отчет о выводе средств:\n"
                                                               f"👤 Пользователю: @{user_db.user_name}\n"
                                                               f"💳 Было выплачено: {money} ₽\n"
                                                               f"🧾 На реквизит: {withdraw_db.withdraw_number}\n"
                                                               f"🆔 По заявке: {withdraw_id}\n"
                                                               f"🕙 Дата вывода: {formatted_date}\n"
                                                               f"✅ Статус: {withdraw_db.withdraw_status}\n")

    await bot.send_message(chat_id=user_id, text="✅ Ваша заявка на вывод была успешно обработана , ожидайте поступление денежных средств.")


