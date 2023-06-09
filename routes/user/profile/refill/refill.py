# import json
#
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from database.db_commands import DBCommands
# from database.models.user import User
# from misc.states import UserState
# from utils.misc.kb_config import qiwi_btn, lolz_btn
# from utils.payments import qiwi, lzt
# from utils.payments.lzt import Lolz
# from utils.payments.qiwi import QiwiAPI
#
#
# async def chose_refill_type_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
#     await state.clear()
#     inline_keyboard = [
#         [InlineKeyboardButton(text=qiwi_btn, callback_data=f"refill_type:qiwi"),
#          ],
#         [InlineKeyboardButton(text=lolz_btn, callback_data=f"refill_type:lolz"),
#          ]
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
#     await call.message.edit_text("Выберите тип пополнения:", reply_markup=keyboard)
#
#
# async def ask_refill_count_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
#     await state.update_data(refill_type=call.data.split(":")[1])
#     await call.message.edit_text("Введите сумму пополнения: (от 50 рублей)")
#     await state.set_state(UserState.refill_count)
#
#
# async def get_refill_count_handler(message: Message, state: FSMContext, session: AsyncSession):
#     if message.text.isdigit():
#         if int(message.text) >= 50:
#             refill_type = (await state.get_data())['refill_type']
#             if refill_type == 'qiwi':
#                 get_message, get_link, receipt = await (
#                     await QiwiAPI()
#                 ).bill_pay(int(message.text))
#             else:
#                 lzt = await Lolz()
#                 receipt = lzt.get_random_string().split('.')[1]
#                 get_link, get_message = await lzt.get_link(int(message.text), receipt)
#
#             inline_keyboard = [
#                 [InlineKeyboardButton(text="Оплатить", url=get_link),
#                  ],
#                 [InlineKeyboardButton(text="Проверить оплату", callback_data=f"check_pay:{refill_type}:{receipt}:{message.text}")]
#             ]
#             keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
#             await message.answer(get_message, reply_markup=keyboard)
#         else:
#             await message.delete()
#             # await message.answer("Минимальная сумма 50 рублей")
#
#     else:
#         await message.edit_text("Введите число")
#
# async def check_pay_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
#     refill_type = call.data.split(":")[1]
#     receipt = call.data.split(":")[2]
#     amount = int(call.data.split(":")[3])
#     if refill_type == 'qiwi':
#         pay_status, pay_amount = await (
#             await QiwiAPI()
#         ).check_form(receipt)
#
#         if pay_status == "PAID":
#             user_db = await DBCommands(User, session).get(user_id=call.from_user.id)
#             await DBCommands(User, session).update(values=dict(balance=user_db.balance + pay_amount,
#                                                                total_balance=
#                                                                    user_db.total_balance + pay_amount),
#                                                    where=dict(user_id=call.from_user.id))
#             if user_db.referrer_id is not None:
#                 referrer = await DBCommands(User, session).get(user_id=user_db.referrer_id)
#                 await DBCommands(User, session).update(values=dict(balance=referrer.balance + pay_amount * 0.15,
#                                                                    total_balance=
#                                                                        referrer.total_balance + pay_amount* 0.15,
#                                                                    refill_from_referrer=referrer.refill_from_referrer + pay_amount* 0.15),
#                                                        where=dict(user_id=user_db.referrer_id))
#             await call.message.edit_reply_markup(None)
#         elif pay_status == "EXPIRED":
#             await call.message.edit_text("<b>❌ Время оплаты вышло. Платёж был удалён.</b>")
#         elif pay_status == "WAITING":
#             await call.answer("❗ Платёж не был найден.\n"
#                               "⌛ Попробуйте чуть позже.", True, cache_time=5)
#         elif pay_status == "REJECTED":
#             await call.message.edit_text("<b>❌ Счёт был отклонён.</b>")
#     else:
#         lolz = await Lolz()
#         if lolz.check_payment(comment=receipt, amount=int(amount)):
#             user_db = await DBCommands(User, session).get(user_id=call.from_user.id)
#             await DBCommands(User, session).update(values=dict(balance=int(user_db.balance + int(amount)),
#                                                                total_balance=int(
#                                                                    user_db.total_balance + int(amount))),
#                                                    where=dict(user_id=call.from_user.id))
#             if user_db.referrer_id is not None:
#                 referrer = await DBCommands(User, session).get(user_id=user_db.referrer_id)
#                 await DBCommands(User, session).update(values=dict(balance=referrer.balance + amount * 0.15,
#                                                                    total_balance=
#                                                                        referrer.total_balance + amount * 0.15,
#                                                                    refill_from_referrer=referrer.refill_from_referrer + amount * 0.15),
#                                                        where=dict(user_id=user_db.referrer_id))
#         else:
#             await call.answer("❗ Платёж не был найден.\n"
#                               "⌛ Попробуйте чуть позже.", True, cache_time=5)