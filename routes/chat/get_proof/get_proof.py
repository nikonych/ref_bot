import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InputMedia
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from misc.states import TokenState


async def get_proof_album_handler(message: Message, album: list[Message], state: FSMContext, bot: Bot, session: AsyncSession):
    media_group = []
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            media_group.append(InputMediaPhoto(media=file_id))
        else:
            obj_dict = msg.dict()
            file_id = obj_dict[msg.content_type]['file_id']
            media_group.append(InputMedia(media=file_id))

    user_id = (await state.get_data()).get('user_id')
    message_id = (await state.get_data()).get('message_id')
    message_text = (await state.get_data()).get('message_text')
    if message.caption is not None:
        if message.caption.isdigit():
            user_db = await DBCommands(User, session).get(user_id=user_id)
            await DBCommands(User, session).update(values=dict(balance=int(user_db.balance + int(message.caption)),
                                                               total_balance=int(
                                                                   user_db.total_balance + int(message.caption))),
                                                   where=dict(user_id=user_id))
            await bot.send_message(chat_id=user_id, text="Отчет о вашем файле:")
            await bot.send_media_group(chat_id=user_id, media=media_group)
            await bot.send_message(chat_id=user_id, text="Ваши токены были отработаны: \n"
                                                         f"Вам начислено: {message.caption}₽")
            with open("database/settings.json", "r") as read_file:
                data = json.load(read_file)

            await bot.edit_message_reply_markup(chat_id=data['chat_id'],
                                                message_id=message_id, reply_markup=None)
            await bot.edit_message_caption(chat_id=data['chat_id'],
                                           message_id=message_id, caption=message_text + "\n\n"
                                                                                         f"Выдано: {message.caption}₽\n"
                                                                                         f"Отчет был отправлен.")
            messages_id = (await state.get_data()).get("messages_id")
            for m_id in messages_id:
                await bot.delete_message(chat_id=data['chat_id'], message_id=m_id)
            await bot.delete_message(chat_id=data['chat_id'], message_id=message.message_id)
        else:
            msg = await message.answer("Введите сумму")
            await state.update_data(messages_id=(await state.get_data()).get("messages_id").append(msg.message_id))
            await bot.send_message(chat_id=user_id, text="Отчет о вашем файле:")
            await bot.send_media_group(chat_id=user_id, media=media_group)
            await state.update_data(message_text=message_text)
            await state.set_state(TokenState.money)
    else:
        msg = await message.answer("Введите сумму")
        messages_id = (await state.get_data()).get("messages_id")
        messages_id.append(msg.message_id)
        messages_id.append(message.message_id)
        print(messages_id)
        await state.update_data(messages_id=messages_id)
        await bot.send_message(chat_id=user_id, text="Отчет о вашем файле:")
        await bot.send_media_group(chat_id=user_id, media=media_group)
        await state.update_data(message_text=message_text)
        await state.set_state(TokenState.money)


# async def get_proof_handler(message: Message, state: FSMContext, bot: Bot, session: AsyncSession):
#
#     user_id = (await state.get_data()).get('user_id')
#     message_id = (await state.get_data()).get('message_id')
#     message_text = (await state.get_data()).get('message_text')
#     if message.caption is not None:
#         if message.caption.isdigit():
#             user_db = await DBCommands(User, session).get(user_id=user_id)
#             await DBCommands(User, session).update(values=dict(balance=int(user_db.balance + int(message.caption)),
#                                                                total_balance=int(
#                                                                    user_db.total_balance + int(message.caption))),
#                                                    where=dict(user_id=user_id))
#             await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id)
#             await bot.send_message(chat_id=user_id, text="Ваши токены были отработаны: \n"
#                                                          f"Вам начислено: {message.caption}₽")
#             with open("database/settings.json", "r") as read_file:
#                 data = json.load(read_file)
#
#             await bot.edit_message_reply_markup(chat_id=data['chat_id'],
#                                                 message_id=message_id, reply_markup=None)
#             await bot.edit_message_caption(chat_id=data['chat_id'],
#                                            message_id=message_id, caption=message_text + "\n\n"
#                                                                                          f"Выдано: {message.caption}₽\n"
#                                                                                          f"Отчет был отправлен.")
#         else:
#             await message.answer("Введите сумму")
#             await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id)
#             await state.update_data(message_text=message_text + "\n\n"
#                                                                 "Отчет был отправлен")
#             await state.set_state(TokenState.money)
#     else:
#         await message.answer("Введите сумму")
#         await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id)
#         await state.update_data(message_text=message_text + "\n\n"
#                                                             "Отчет был отправлен")
#         await state.set_state(TokenState.money)
