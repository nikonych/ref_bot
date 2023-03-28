import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from misc.states import TokenState


async def add_balance_handler(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
    user_id = (await state.get_data()).get('user_id')
    message_id = (await state.get_data()).get('message_id')
    message_text = (await state.get_data()).get('message_text')
    check_type = (await state.get_data()).get('check_type')
    if check_type == "no":
        user_db = await DBCommands(User, session).get(user_id=user_id)
        if message.text.isdigit():
            await DBCommands(User, session).update(values=dict(balance=int(user_db.balance + int(message.text)),
                                                               total_balance=int(
                                                                   user_db.total_balance + int(message.text))),
                                                   where=dict(user_id=user_id))
            with open("database/settings.json", "r") as read_file:
                data = json.load(read_file)
            await bot.edit_message_reply_markup(chat_id=data['chat_id'],
                                                message_id=message_id, reply_markup=None)
            await bot.edit_message_caption(chat_id=data['chat_id'],
                                                message_id=message_id, caption=message_text + "\n"
                                                                                              "✅Отработано\n"
                                                                                              f"💳 Выдано: {message.text}₽")
            await bot.send_message(chat_id=user_id, text="✅ Ваши токены успешно отработаны! \n"
                                                         f"💳 Ваша выплата составляет: {message.text}₽")
            messages_id = (await state.get_data()).get("messages_id")

            for m_id in messages_id:
                await bot.delete_message(chat_id=data['chat_id'], message_id=m_id)
            await bot.delete_message(chat_id=data['chat_id'], message_id=message.message_id)
        else:
            await message.delete()
            await state.set_state(TokenState.money)
    else:
        msg = await message.answer("📁 Прикрепите скриншот отчета отработки токенов!")
        await state.update_data(money=message.text)
        msgs = (await state.get_data()).get("messages_id")
        if msgs is not None:
            msgs.extend([message.message_id, msg.message_id])
        print(msgs)
        await state.update_data(messages_id=msgs)
        await state.set_state(TokenState.proof)
