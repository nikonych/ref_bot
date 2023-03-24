import json
from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from utils.misc.kb_config import add_money_btn, empty_btn, send_proof_btn


async def get_file_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot, ):
    user_id = message.from_user.id
    check_type = (await state.get_data()).get('proof')
    text = f"Пользователь: {message.from_user.username}\n" \
           f"ID: {message.from_user.id}\n" \
           f"Полный отчет: {'Да' if check_type == 'yes' else 'Нет'}\n" \
           f"Дата: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
    inline_keyboard = [
        [InlineKeyboardButton(text=add_money_btn, callback_data=f"add_money:{user_id}:{check_type}"),
         InlineKeyboardButton(text=empty_btn, callback_data=f"empty:{user_id}:{check_type}")],
    ]
    if check_type == "yes":
        inline_keyboard.append(
            [InlineKeyboardButton(text=send_proof_btn, callback_data=f"send_proof:{user_id}:{check_type}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    with open("database/settings.json", "r") as read_file:
        data = json.load(read_file)

    await bot.send_document(chat_id=data['chat_id'], document=message.document.file_id,
                            caption=text, reply_markup=keyboard)
    await message.answer("Ваши токены были успешно загружены! Ожидайте результата!")
    user_db = await DBCommands(User, session).get(user_id=user_id)
    await DBCommands(User, session).update(values=dict(token_count=int(user_db.token_count) + 1),
                                           where=dict(user_id=user_id))

# async def get_file_handler(message: Message, state: FSMContext, session: AsyncSession, album: list[Message], bot: Bot,):
#
#     user_id = message.from_user.id
#
#     media_group = []
#     for msg in album:
#         if msg.photo:
#             file_id = msg.photo[-1].file_id
#             media_group.append(InputMediaPhoto(media=file_id))
#         else:
#             obj_dict = msg.dict()
#             file_id = obj_dict[msg.content_type]['file_id']
#             media_group.append(InputMedia(media=file_id))
#     # await message.answer_media_group(media_group)
#     with open("database/settings.json", "r") as read_file:
#         data = json.load(read_file)
#     await bot.send_media_group(chat_id=data['chat_id'], media=media_group)
