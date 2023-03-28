import json
from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from utils.misc.kb_config import error_number_btn, auto_withdraw_btn, had_withdraw_btn


async def ask_withdraw_money_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    type = None
    user_db = await DBCommands(User, session).get(user_id=message.from_user.id)
    if message.text.isdigit():
        if 50 <= int(message.text) <= int(user_db.balance) <= 10000:
        # if int(message.text) <= int(user_db.balance):
            with open("database/settings.json", "r") as read_file:
                data = json.load(read_file)
            match (await state.get_data()).get("type"):
                case 'qiwi':
                    type = "QIWI"
                case 'lzt':
                    type = "LOLZ"
                case 'yoomoney':
                    type = "YooMoney"
                case 'bank':
                    type = "Bank Card"

            # if type != "LOLZ":
            text = f"👤 Пользователь: {message.from_user.username}\n" \
                   f"🆔 ID: {message.from_user.id}\n\n"
            if type == "QIWI":
                text += f"🥝Вывод на: {type}\n"
            else:
                text += f"💳 Вывод на: {type}\n"

            text +=f"🪪 Реквизит: {(await state.get_data()).get('number')}\n" \
                   f"💳 Сумма: {message.text}₽\n\n" \
                   f"⏰ Дата: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
            # else:
            #     text = f"👤 Пользователь: {message.from_user.username}\n" \
            #            f"🆔 ID: {message.from_user.id}\n\n"
            #     if type == "QIWI":
            #         text += f"🥝Вывод на: {type}\n"
            #     else:
            #         text += f"💳 Вывод на: {type}\n"
            #
            #     text += f"🪪 Реквизит: {(await state.get_data()).get('number')}\n" \
            #            f"🕵 Имя: {(await state.get_data()).get('user_name')}\n" \
            #            f"💳 Сумма: {message.text}₽\n\n" \
            #            f"⏰ Дата: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=error_number_btn, callback_data=f"error_number:{message.from_user.id}:{type}:{message.text}")],
                [InlineKeyboardButton(text=had_withdraw_btn, callback_data=f"had_withdraw:{message.from_user.id}:{message.text}")]
            ])
            # if type != "Bank Card" and type != "LOLZ":
            #     keyboard.inline_keyboard.append([InlineKeyboardButton(text=auto_withdraw_btn, callback_data=f"auto_withdraw:{message.from_user.id}:{type}:{(await state.get_data()).get('number')}:{message.text}")])
            # elif type == "LOLZ":
            #     keyboard.inline_keyboard.append([InlineKeyboardButton(text=auto_withdraw_btn, callback_data=f"auto_withdraw:{message.from_user.id}:{type}:{(await state.get_data()).get('number')}:{(await state.get_data()).get('user_name')}:{message.text}")])
            await bot.send_message(chat_id=data['chat_id'], text=text, reply_markup=keyboard)
            await message.answer(
                "✅ Ваша заявка на вывод средств успешно создана!"
                " Ожидайте поступление средств!")
            await DBCommands(User, session).update(values=dict(balance=int(user_db.balance - int(message.text)),
                                                               wait_balance=int(
                                                                   user_db.wait_balance + int(message.text))),
                                                   where=dict(user_id=message.from_user.id))

            await state.clear()

        else:
            if int(message.text) > int(user_db.balance):
                await message.answer("⚠️ У вас недостаточно средств")
            else:
                if int(message.text) > 10000:
                    await message.answer("⚠️ Максимальная сумма вывода составляет: 10000 ₽")
                else:
                    await message.answer("⚠️ Минимальная сумма вывода составляет 50 ₽")
    else:
        await message.answer("⚠️ Минимальная сумма вывода составляет 50 ₽")
