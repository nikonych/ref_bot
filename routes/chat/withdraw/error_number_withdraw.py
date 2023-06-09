from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from utils.misc.kb_config import qiwi_btn, lolz_btn, yoomoney_btn, bank_card_btn, back_btn


async def error_number_withdraw_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    user_id = int(call.data.split(":")[1])
    type = call.data.split(":")[2]
    money = int(call.data.split(":")[3])
    await call.message.edit_text(call.message.text + "\n\n"
                                                     "❌ Неверные реквизиты", reply_markup=None)
    await bot.send_message(chat_id=user_id, text=f"❌ К сожелению мы не смогли обработать вашу заявку на вывод средств, пожалуйста измените реквизиты и подайте заявку снова!")
    user_db = await DBCommands(User, session).get(user_id=user_id)
    await DBCommands(User, session).update(values=dict(balance=user_db.balance + int(money), wait_balance=user_db.wait_balance - int(money)), where=dict(user_id=user_id))
