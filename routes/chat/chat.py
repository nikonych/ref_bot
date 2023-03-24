# import asyncio
# from typing import List, Union, Dict
# from uuid import uuid4
#
# from aiogram import types, BaseMiddleware
# from aiogram.dispatcher.event.bases import CancelHandler
# from aiogram.enums import ContentType
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, CallbackQuery
#
# from aiogram.types.base import TelegramObject
# from trio._highlevel_open_tcp_stream import DEFAULT_DELAY
#
# from data.dbhandler import update_user, get_settings, get_user
# from keyboards.user_inline import get_are_you_sure_inl, get_check_file_inl
# from loader import dp, bot
# import asyncio
# from typing import Any, Awaitable, Callable, Dict, List, Union
# from aiogram_media_group import media_group_handler
#
#
# class AlbumMiddleware(BaseMiddleware):
#     """This middleware is for capturing media groups."""
#
#     album_data: dict = {}
#
#     def __init__(self, latency: Union[int, float] = 0.01):
#         """
#         You can provide custom latency to make sure
#         albums are handled properly in highload.
#         """
#         self.latency = latency
#         super().__init__()
#
#     async def on_process_message(self, message: Message, data: dict):
#         if not message.media_group_id:
#             return
#
#         try:
#             self.album_data[message.media_group_id].append(message)
#             raise CancelHandler()  # Tell aiogram to cancel handler for this group element
#         except KeyError:
#             self.album_data[message.media_group_id] = [message]
#             await asyncio.sleep(self.latency)
#
#             message.conf["is_last"] = True
#             data["album"] = self.album_data[message.media_group_id]
#
#     async def on_post_process_message(self, message: Message, result: dict, data: dict):
#         """Clean up after handling our album."""
#         if message.media_group_id and message.conf.get("is_last"):
#             del self.album_data[message.media_group_id]
#
#
# @dp.callback_query_handler(text_startswith="empty:", state="*")
# async def gg(call: CallbackQuery, state: FSMContext):
#     user_id = int(call.data.split(":")[1])
#     check_type = call.data.split(":")[2]
#     await call.message.edit_caption(caption=call.message.caption + "\n\n"
#                                                                    "Вы уверены что токены пустые?",
#                                     reply_markup=get_are_you_sure_inl(user_id, check_type))
#
#     # await bot.send_message(chat_id=user_id, text="Ваши токены оказались пустыми!")
#
#
# @dp.callback_query_handler(text_startswith="sure:", state="*")
# async def gg(call: CallbackQuery, state: FSMContext):
#     user_id = int(call.data.split(":")[2])
#     check_type = call.data.split(":")[3]
#     if call.data.split(":")[1] == 'no':
#         await call.message.edit_caption(caption=call.message.caption.split("\n\n")[0],
#                                         reply_markup=get_check_file_inl(check_type, user_id))
#     else:
#         await bot.send_message(chat_id=user_id, text="Ваши токены оказались пустыми!")
#         await call.message.edit_caption(caption=call.message.caption.split("\n\n")[0])
#         await call.message.delete_reply_markup()
#
#
# @dp.callback_query_handler(text_startswith="add_money:", state="*")
# async def gg(call: CallbackQuery, state: FSMContext):
#     user_id = int(call.data.split(":")[1])
#     message_id = call.message.message_id
#     await call.message.answer("Введите сумму")
#     await state.update_data(user_id=user_id)
#     await state.update_data(message_id=message_id)
#     await state.set_state("wait_money")
#
#
# @dp.message_handler(state='wait_money')
# async def gg(message: Message, state: FSMContext):
#     if message.text.isdigit():
#         update_user(user_id=(await state.get_data())['user_id'],
#                     balance=get_user(user_id=(await state.get_data())['user_id'])['balance'] + int(message.text),
#                     total_balance=get_user(user_id=(await state.get_data())['user_id'])['total_balance'] + int(
#                         message.text))
#         await bot.edit_message_reply_markup(chat_id=get_settings()['botchat'],
#                                             message_id=(await state.get_data())['message_id'], reply_markup=None)
#         await bot.send_message(chat_id=(await state.get_data())['user_id'], text="Ваши токены были отработаны: \n"
#                                                                                  f"Вам начислено: {message.text}₽")
#     else:
#         await message.delete()
#         await state.set_state("wait_money")
#
#
# @dp.callback_query_handler(text_startswith="send_proof:", state="*")
# async def gg(call: CallbackQuery, state: FSMContext):
#     user_id = int(call.data.split(":")[1])
#     await call.message.answer("Отправьте фотографии с отчетом и сумму")
#     message_id = call.message.message_id
#     await state.update_data(user_id=user_id)
#     await state.update_data(message_id=message_id)
#     await state.set_state("wait_proof")
#
#
#
# @dp.message_handler(is_media_group=True, content_types=types.ContentType.ANY)
# async def handle_albums(message: types.Message, album: List[types.Message]):
#     print(message.photo)
#
# @dp.message_handler(is_media_group=True, state='wait_proof', content_types=ContentType.ANY)
# async def gg(message: Message, album: List[types.Message], state: FSMContext):
#     media_group = types.MediaGroup()
#     for obj in album:
#         if obj.photo:
#             file_id = obj.photo[-1].file_id
#         else:
#             file_id = obj[obj.content_type].file_id
#
#         try:
#             # We can also add a caption to each file by specifying `"caption": "text"`
#             media_group.attach({"media": file_id, "type": obj.content_type})
#         except ValueError:
#             return await message.answer("This type of album is not supported by aiogram.")
#
#     await message.answer_media_group(media_group)
#
#     # if message.caption is not None:
#     #     if message.caption.isdigit():
#     #         update_user(user_id=(await state.get_data())['user_id'],
#     #                     balance=get_user(user_id=(await state.get_data())['user_id'])['balance'] + int(message.caption),
#     #                     total_balance=get_user(user_id=(await state.get_data())['user_id'])['total_balance'] + int(message.caption))
#     #         await bot.send_media_group(chat_id=(await state.get_data())['user_id'], media=media_group)
#     #         await bot.send_message(chat_id=(await state.get_data())['user_id'], text="Ваши токены были отработаны: \n"
#     #                                                                                  f"Вам начислено: {message.caption}₽")
#     #     else:
#     #         await message.answer("Введите сумму")
#     #         await bot.send_media_group(chat_id=(await state.get_data())['user_id'], media=media_group)
#     #         await state.set_state("wait_money")
#     # else:
#     #     await message.answer("Введите сумму")
#     #     await bot.send_media_group(chat_id=(await state.get_data())['user_id'], media=media_group)
#     #     await state.set_state("wait_money")
