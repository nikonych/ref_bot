# - *- coding: utf- 8 - *-
import asyncio
import datetime
import os
from typing import Union

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType
# from dateutil import relativedelta

from data import config
# from tgbot.data.config import bot_description
from keyboards.inline_user import profile_buttons, top_buttons, back_button_to_profile, choose_withdraw, withdraw_admin_buttons
from .user import get_profile_text
# from tgbot.keyboards.inline_z_page import *
from keyboards.reply_z_all import menu_frep
from loader import dp, bot
# from tgbot.services.api_sqlite import *
from utils.const_functions import get_date, split_messages, get_unix
# from tgbot.utils.misc.bot_filters import IsBan, IsAdmin, IsChat
# from tgbot.utils.misc_functions import open_profile_my, upload_text, get_faq, get_vip_text
import services.dbhandler as db




# Настройка отработки
@dp.callback_query_handler(text_startswith="otrabotka_settings:", state="*")
async def back_to_profile(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    await state.finish()
    user_id = int(message.data.split(":")[1])
    user_data = db.get_userx(user_id=user_id)
    await message.answer("⚙️ В разработке")

# Кнопка назад в профиль
@dp.callback_query_handler(text="user_profile", state="*")
async def back_to_profile(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    await state.finish()
    user_data = db.get_userx(user_id=message.from_user.id)
    await bot.send_message(message.from_user.id,await get_profile_text(user_data), reply_markup=await profile_buttons(user_data))
    await message.message.delete()

# Вывод средств
@dp.callback_query_handler(text_startswith="withdraw:", state="*")
async def balance_withdraw(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    await state.finish()
    user_id = int(message.data.split(":")[1])
    user_data = db.get_userx(user_id=user_id)
    user_balance = user_data['user_balance']
    if user_balance > config.min_withdraw:
        await bot.send_message(user_id,f"Максимально вы можете вывести <b>{user_balance}$.</b>"
                             f"\n<b>Введите сумму вывода:</b>", reply_markup= await back_button_to_profile())
        await state.set_state('wait_balance_for_withdraw')
        await state.update_data(user_id=user_id)
    else: await bot.send_message(user_id,f"<b>❗ Ваш баланс меньше минимальной суммы вывода ({config.min_withdraw}$) </b>")

@dp.message_handler(state='wait_balance_for_withdraw')
async def balance_for_withdraw(message: Message, state: FSMContext):
    user_data = db.get_userx(user_id=(await state.get_data())['user_id'])
    user_balance = user_data['user_balance']
    try:
        howmany = int(message.text)
    except:
        await message.answer('🔴 Неправильный ввод. Введите еще раз.', reply_markup=await back_button_to_profile())
        return None

    if user_balance >= int(message.text):
        await message.answer('⚡️Выберите куда вывести средства:', reply_markup=await choose_withdraw())
        await state.set_state('where_to_withdraw')
        await state.update_data(howmany=int(message.text))
    else:
        await message.answer(f'🔴 Максимально вы можете вывести <b>{user_balance}$</b>. Введите еще раз.', reply_markup=await back_button_to_profile())
        return None

@dp.callback_query_handler(text_startswith="withdraw_to:", state="where_to_withdraw")
async def withdraw_to(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    where = message.data.split(":")[1]
    howmany = (await state.get_data())['howmany']
    await message.message.edit_text("🖍 Введите реквизиты для вывода:")
    await state.set_state('withdraw_prop')
    await state.update_data(where=where,howmany=howmany)

@dp.message_handler(state='withdraw_prop')
async def withdraw_prop(message: Message, state: FSMContext):
    where = (await state.get_data())['where']
    howmany = (await state.get_data())['howmany']
    to_prop = message.text
    user_data = db.get_userx(user_id=(await state.get_data())['user_id'])
    db.update_userx(user_id=message.from_user.id, user_balance=user_data['user_balance']-howmany)
    await bot.send_message(db.get_settings()['adminchat'], f"‼️ Заявка на вывод средств.\n"
                                                           f"\n"
                                                           f"📝 Информация о выводе:\n"
                                                           f"  💸 Сумма: {howmany}$.\n"
                                                           f"  💰 Сервис: {where}.\n"
                                                           f"  💳 Реквизиты кошелька: {to_prop}", reply_markup=await withdraw_admin_buttons([message.from_user.id, howmany]))

    await message.answer(f"✅ Ваш вывод средств отправлен на обработку.\n"
                         f"\n"
                         f"📝 Информация о выводе:\n"
                         f"  💸 Сумма: {howmany}$.\n"
                         f"  💰 Сервис: {where}.\n"
                         f"  💳 Реквизиты кошелька: {to_prop}")





# Скрытие профиля
@dp.callback_query_handler(text_startswith="hide_username", state="*")
async def hide_username(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    await state.finish()
    user_id = int(message.data.split(":")[1])
    db.update_userx(is_visible=False, user_id=user_id)
    await message.message.edit_text(await get_profile_text(db.get_userx(user_id=message.from_user.id)),reply_markup=await profile_buttons(db.get_userx(user_id=message.from_user.id)))

# Показ профиля
@dp.callback_query_handler(text_startswith="show_username", state="*")
async def show_username(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    await state.finish()
    user_id = int(message.data.split(":")[1])
    db.update_userx(is_visible=True, user_id=user_id)
    await message.message.edit_text(await get_profile_text(db.get_userx(user_id=message.from_user.id)),
                                    reply_markup=await profile_buttons(db.get_userx(user_id=message.from_user.id)))

# Обновление Юзернейма
@dp.callback_query_handler(text_startswith="refresh_username", state="*")
async def show_username(message: Union['Message', 'CallbackQuery'], state: FSMContext):
    await state.finish()
    user_id = int(message.data.split(":")[1])
    db.update_userx(user_login=message.from_user.username, user_name=message.from_user.full_name, user_id=user_id)
    await message.message.edit_text(await get_profile_text(db.get_userx(user_id=message.from_user.id)),
                                    reply_markup=await profile_buttons(db.get_userx(user_id=message.from_user.id)))

#
# # Открытие товаров
# @dp.message_handler( IsChat(), IsBan(),text="🛍 Товары", state="*")
# async def user_shop(message: Message, state: FSMContext):
#     await state.finish()
#
#     if len(get_all_categoriesx()) >= 1:
#         await message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption="<b>🎁 Выберите нужный вам товар:</b>",
#                                    reply_markup=products_item_category_open_fp(0))
#     else:
#         await message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption="<b>🎁 Товары в данное время отсутствуют.</b>")
#
#
# # Открытие профиля
# @dp.message_handler( IsChat(), IsBan(), text="👮‍♀️ Профиль", state="*")
# async def user_profile(message: Message, state: FSMContext):
#     await state.finish()
#     me = await bot.get_me()
#     await message.answer_photo(open('tgbot/data/resourses/photo/profile.jpg', 'rb'), caption=open_profile_my(message.from_user.id, me), reply_markup=profile_open_inl)
#
#
# # Открытие FAQ
# @dp.message_handler( IsChat(), IsBan(), text=["📕 Правила", "/faq"], state="*")
# async def user_faq(message: Message, state: FSMContext):
#     await state.finish()
#
#     send_message = get_settingsx()['misc_faq']
#     if send_message == "None":
#         send_message = f"ℹ Информация. Измените её в настройках бота.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{bot_description}"
#
#     await message.answer_photo(open('tgbot/data/resourses/photo/rule.jpg', 'rb'),
#                                caption=get_faq(message.from_user.id, send_message), reply_markup=close_inl)
#
#
#
# # Открытие сообщения с ссылкой на поддержку
# @dp.message_handler( IsChat(), IsBan(), text=["☎ Поддержка", "/support"], state="*")
# async def user_support(message: Message, state: FSMContext):
#     await state.finish()
#
#
#     await message.answer_photo(open('tgbot/data/resourses/photo/help.jpg', 'rb'),
#                                caption="<b>☎️ Нажмите на кнопку ниже, чтобы связаться с Администрацией магазина!</b>",
#                                reply_markup=user_support_finl())
#
#
#
# @dp.callback_query_handler( IsChat(), text_startswith="links_to_admins", state="*")
# async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
#     user_admin = get_settingsx()['misc_support']
#     user_support = get_settingsx()['misc_support_two']
#     if str(user_support).isdigit() and str(user_admin).isdigit():
#         get_admin = get_userx(user_id=user_admin)
#         get_support = get_userx(user_id=user_support)
#         if len(get_admin['user_login']) >= 1 and len(get_support['user_login']) >= 1:
#             await call.message.edit_reply_markup(reply_markup=admin_support_finl(get_admin['user_login'], get_support['user_login']))
#
# @dp.callback_query_handler( IsChat(), text_startswith="open_faq", state="*")
# async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#
#     await call.message.edit_caption(
#                                caption="<b>☎️ Нажмите на кнопку ниже, чтобы связаться с Администрацией магазина!</b>",
#                                reply_markup=user_support_finl())
# ################################################################################################
# # Просмотр истории покупок
# @dp.callback_query_handler( IsChat(), text="user_history", state="*")
# async def user_history(call: CallbackQuery, state: FSMContext):
#     last_purchases = last_purchasesx(call.from_user.id, 5)
#
#     if len(last_purchases) >= 1:
#         await call.answer("🎁 Последние 5 покупок")
#         await call.message.delete()
#
#         for purchases in last_purchases:
#             link_items = await upload_text(call, purchases['purchase_item'])
#
#             await call.message.answer(f"<b>🧾 Чек: <code>#{purchases['purchase_receipt']}</code></b>\n"
#                                       f"🎁 Товар: <code>{purchases['purchase_position_name']} | {purchases['purchase_count']}шт | {purchases['purchase_price']}₽</code>\n"
#                                       f"🕰 Дата покупки: <code>{purchases['purchase_date']}</code>\n"
#                                       f"🎁 Товары: <a href='{link_items}'>кликабельно</a>")
#
#             try:
#                 print(purchases['purchase_item'])
#                 for item in purchases['purchase_item'].split('\n'):
#                     print(item)
#                     item = item.split()[1]
#                     if os.path.isfile(f"tgbot/data/items/{item}"):
#                         await bot.send_document(call.from_user.id, open(f"tgbot/data/items/{item}", 'rb'))
#             except:
#                 pass
#
#         await call.message.answer(open_profile_my(call.from_user.id), reply_markup=profile_open_inl)
#     else:
#         await call.answer("❗ У вас отсутствуют покупки", True)
#
#
# @dp.callback_query_handler( IsChat(), text="show_referer", state="*")
# async def show_referer(call: CallbackQuery, state: FSMContext):
#     referers = get_usersx(user_referer=call.from_user.id)
#     if referers is not None and referers != []:
#         limit = 10
#         count = 0
#         # await call.message.edit_caption("🎁 Ваши рефералы:\n" \
#         #                             "👤 Имя  | 🎩 Статус | 💳  Пополнено | 💹  Ваша доля")
#         text = "🎁 Ваши рефералы:\n" \
#                                     "👤 Имя  | 🎩 Статус | 💳  Пополнено | 💹  Ваша доля\n\n\n"
#         for a in range(0, len(referers)):
#             if a < limit:
#                 text += f"👤 @{referers[a]['user_login']} | 🎩 {referers[a]['user_role']} | 💳 {referers[a]['user_refill']}₽ | 💹 {int(referers[a]['user_refill']*0.05)}₽\n" \
#                     f"———————————————————————-\n"
#                 count += 1
#             else:
#                 break
#         if len(referers) < limit:
#             await call.message.edit_caption(text, reply_markup=close_inl)
#         else:
#             await call.message.edit_caption(text, reply_markup=get_referer_list_nextp(count))
#     else:
#         await call.answer("У вас нету рефераллов!")
#
#
# @dp.callback_query_handler( IsChat(), text_startswith="referer_list_nextp", state="*")
# async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#     referers = get_usersx(user_referer=call.from_user.id)
#     limit = 10 + remover
#     text = "🎁 Ваши рефералы:\n" \
#            "👤 Имя  | 🎩 Статус | 💳  Пополнено | 💹  Ваша доля\n\n\n"
#     count = 0
#     for a in range(remover, len(referers)):
#         if a < limit:
#             text += f"👤 @{referers[a]['user_login']} | 🎩 {referers[a]['user_role']} | 💳 {referers[a]['user_refill']}₽ | 💹 {int(referers[a]['user_refill'] * 0.05)}₽\n" \
#                     f"———————————————————————-\n"
#             count += 1
#         else:
#             break
#     if count + remover == len(referers):
#         await call.message.edit_caption(text, reply_markup=get_referer_list_backp(remover-10))
#     else:
#         await call.message.edit_caption(text, reply_markup=get_referer_list_medp(remover))
#
# @dp.callback_query_handler( IsChat(), text_startswith="referer_list_backp", state="*")
# async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#     referers = get_usersx(user_referer=call.from_user.id)
#     limit = 10 + remover
#     text = "🎁 Ваши рефералы:\n" \
#            "👤 Имя  | 🎩 Статус | 💳  Пополнено | 💹  Ваша доля\n\n\n"
#     count = 0
#     for a in range(remover, len(referers)):
#         if a < limit:
#             text += f"👤 @{referers[a]['user_login']} | 🎩 {referers[a]['user_role']} | 💳 {referers[a]['user_refill']}₽ | 💹 {int(referers[a]['user_refill'] * 0.05)}₽\n" \
#                     f"———————————————————————-\n"
#             count += 1
#         else:
#             break
#     if remover == 0:
#         await call.message.edit_caption(text, reply_markup=get_referer_list_nextp(count))
#     elif count + remover == len(referers):
#         await call.message.edit_caption(text, reply_markup=get_referer_list_backp(remover - limit))
#     else:
#         await call.message.edit_caption(text, reply_markup=get_referer_list_medp(remover))
#
# @dp.callback_query_handler( IsChat(), text="buy_vip", state="*")
# async def user_buy_vip(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#
#     send_message = get_settingsx()['misc_vip']
#     if send_message == "None" or send_message == None or send_message == 'vip':
#         send_message = f"ℹ Информация. Измените её в настройках бота.\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{bot_description}"
#     send_message = get_vip_text(send_message)
#     await call.message.edit_caption(
#                                caption=send_message, reply_markup=buy_vip_inl_())
#
#
# @dp.callback_query_handler( IsChat(), text="buy_vip_money", state="*")
# async def user_buy_vip(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#     settings = get_settingsx()
#
#     user = get_userx(user_id=call.from_user.id)
#     balance = user['user_balance']
#     nextmonth = datetime.date.today() + relativedelta.relativedelta(months=1)
#     if user['user_role'] != 'VIP' and user['user_role'] != 'Admin' and user['user_role'] != 'Support':
#         if balance >= settings['vip_price']:
#             update_userx(user_id=call.from_user.id, user_balance=balance-settings['vip_price'], user_role='VIP', vip_date=nextmonth)
#             await call.answer("🎁 Покупка прошла успешно!")
#             me = await bot.get_me()
#             await call.message.edit_caption(caption=open_profile_my(call.from_user.id, me), reply_markup=profile_open_inl)
#         else:
#             await call.answer("❗ У вас недостаточно средств!")
#             get_kb = refill_choice_finl()
#
#             if get_kb is not None:
#                 await call.message.edit_caption("<b>💳 Выберите способ пополнения</b>",
#                                                 reply_markup=get_kb)
#             else:
#                 await call.answer("⛔ Пополнение временно недоступно", True)
#     elif user['user_role'] == 'Admin':
#         await call.answer("❗ Зачем? Вы же Админ!")
#     elif user['user_role'] == 'Support':
#         await call.answer("❗ Зачем? Вы же Модератор!")
#     else:
#         await call.answer("❗ У вас уже есть VIP!")
#
#
# # Возвращение к профилю
# @dp.callback_query_handler( IsChat(), text="user_profile", state="*")
# async def user_profile_return(message: Union['Message', 'CallbackQuery'], state: FSMContext):
#     me = await bot.get_me()
#     await message.message.edit_caption(open_profile_my(message.from_user.id, me), reply_markup=profile_open_inl)
#
#
# # Referer system
# @dp.message_handler( IsChat(), IsBan(), text="🎁 Реферальная система")
# async def user_referer(message: Message, state: FSMContext):
#     percent = config.PERCENT
#     me = await bot.get_me()
#     user_id = message.from_user.id
#     link = 'https://t.me/' + me.username + '?start=' + str(user_id)
#     await message.answer_photo(open('tgbot/data/resourses/photo/referer.jpg', 'rb'),
#                                caption=
#                                f'💙 Реферальная система 💙\n'
#                                '\n'
#                                '🔗 Ваша персональная ссылка:\n'
#                                f'<code>{link}</code>\n'
#                                f'\n'
#                                f'1️⃣ Вам нужно скопировать ссылку и поделиться  ей с  другом или знакомым!\n'\
#                                f'2️⃣ После того, как ваш друг или знакомый пополнит баланс - вам будет автоматически начислено {percent}% на ваш баланс от его пополнения!\n'
#                                f'3️⃣ Для вывода средств с вашего баланса вам нужно в чате с поддержкой указать ваш ID в боте! Сумма для вывода средств с баланса - не менее 300р!!\n',
#                                reply_markup=close_inl
#                                )
#
#
# ################################################################################################
# ######################################### ПОКУПКА ТОВАРА #######################################
# ########################################### КАТЕГОРИИ ##########################################
# # Открытие категорий для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_category_open", state="*")
# async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
#     category_id = int(call.data.split(":")[1])
#
#     get_category = get_categoryx(category_id=category_id)
#     # get_positions = get_positionsx(category_id=category_id)
#     get_subcategory = get_subcategoriesx(category_id=category_id)
#
#
#     if len(get_subcategory) + len(get_positionsx(category_id=category_id, subcategory_id=0)) >= 1:
#         await call.message.edit_caption("<b>🎁 Выберите нужную вам подкатегорию:</b>",
#                                         reply_markup=products_item_subcategory_open_fp(0, category_id, call.from_user.id))
#         # await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#         #                              reply_markup=products_item_position_open_fp(0, category_id, call.from_user.id))
#     else:
#         await call.answer(f"❕ Подкатегории и позиции в категории {get_category['category_name']} отсутствуют")
#
#
# @dp.callback_query_handler( IsChat(), text_startswith="buy_subcategory_open", state="*")
# async def user_purchase_category_open(call: CallbackQuery, state: FSMContext):
#     subcategory_id = int(call.data.split(":")[1])
#     category_id = int(call.data.split(":")[2])
#
#     get_category = get_subcategoryx(subcategory_id=subcategory_id)
#     get_positions = get_positionsx(subcategory_id=subcategory_id)
#     # get_subcategory = get_subcategoriesx(category_id=category_id)
#
#
#     if len(get_positions) >= 1:
#         await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                      reply_markup=products_item_position_open_fp(0, category_id, call.from_user.id, subcategory_id))
#     else:
#         await call.answer(f"❕ Позиции в подкатегории {get_category['subcategory_name']} отсутствуют")
#
# # Вернуться к категориям для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_category_return", state="*")
# async def user_purchase_category_return(call: CallbackQuery, state: FSMContext):
#     get_categories = get_all_categoriesx()
#
#     if len(get_categories) >= 1:
#         await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                      reply_markup=products_item_category_open_fp(0))
#     else:
#         await call.message.edit_caption("<b>🎁 Товары в данное время отсутствуют.</b>")
#         await call.answer("❗ Категории были изменены или удалены")
#
#
#
#
# # Следующая страница категорий для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_category_nextp", state="*")
# async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#
#     await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                  reply_markup=products_item_category_next_page_fp(remover))
#
# @dp.callback_query_handler( IsChat(), text_startswith="buy_subcategory_nextp", state="*")
# async def user_purchase_category_next_page(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#     category_id = int(call.data.split(":")[2])
#
#
#     await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                  reply_markup=products_item_subcategory_next_page_fp(remover, category_id))
#
#
# # Предыдущая страница категорий для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_category_backp", state="*")
# async def user_purchase_category_prev_page(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#
#     await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                  reply_markup=products_item_category_back_page_fp(remover))
#
# @dp.callback_query_handler( IsChat(), text_startswith="buy_subcategory_backp", state="*")
# async def user_purchase_category_prev_page(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#     category_id = int(call.data.split(":")[2])
#
#     await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                  reply_markup=products_item_subcategory_back_page_fp(remover, category_id))
#
#
# ########################################### ПОЗИЦИИ ##########################################
# # Открытие позиции для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_position_open", state="*")
# async def user_purchase_position_open(call: CallbackQuery, state: FSMContext):
#     position_id = int(call.data.split(":")[1])
#     remover = int(call.data.split(":")[2])
#     category_id = int(call.data.split(":")[3])
#     subcategory_id = int(call.data.split(":")[4])
#     settings = get_settingsx()
#
#     get_user = get_userx(user_id=call.from_user.id)
#     get_position = get_positionx(position_id=position_id)
#     get_category = get_categoryx(category_id=category_id)
#     get_subcategory = get_subcategoryx(subcategory_id=subcategory_id)
#     get_items = get_itemsx(position_id=position_id)
#     if get_user['user_role'] == "VIP" and get_user['is_reseller'] == False:
#         get_position['position_price'] = int(get_position['position_price'] * (100- settings['vip_percent']) * 0.01)
#     elif get_user['user_role'] == "VIP" and get_user['is_reseller'] == True:
#         settings = get_settingsx()
#         get_position['position_price'] = int(get_position['position_price'] * (
#                 100 - settings['vip_percent'] - 15) * 0.01)
#     elif get_user['user_role'] == "Re-Seller":
#         get_position['position_price'] = int(get_position['position_price'] * (
#                 100 - 15) * 0.01)
#     if get_position['position_description'] == "0":
#         text_description = ""
#     else:
#         text_description = f"\n📜 Описание:\n" \
#                            f"{get_position['position_description']}"
#
#     send_msg = f"<b>🎁 Покупка товара:</b>\n" \
#                f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
#                f"🆕 Название: <code>{get_position['position_name']}</code>\n" \
#                f"🗃 Категория: <code>{get_category['category_name']}</code>\n"
#     if get_subcategory is not None:
#         send_msg += f"📘 Подкатегория: <code>{get_subcategory['subcategory_name']}</code>\n"
#     send_msg += f"💳 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
#                f"🆔 Количество: <code>{len(get_items)}шт</code>" \
#                f"{text_description}"
#
#     if len(get_position['position_photo']) >= 5:
#         await call.message.delete()
#         await call.message.answer_photo(get_position['position_photo'],
#                                         send_msg, reply_markup=products_open_finl(call.from_user.id ,position_id, remover, category_id, subcategory_id))
#     else:
#         await call.message.edit_caption(send_msg,
#                                      reply_markup=products_open_finl(call.from_user.id ,position_id, remover, category_id, subcategory_id))
#
#
# # Вернуться к позициям для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_position_return", state="*")
# async def user_purchase_position_return(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#     category_id = int(call.data.split(":")[2])
#     subcategory_id = int(call.data.split(":")[3])
#
#
#     get_positions = get_positionsx(category_id=category_id)
#
#     if len(get_positions) >= 1:
#         await call.message.delete()
#         await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption="<b>🎁 Выберите нужный вам товар:</b>",
#                                   reply_markup=products_item_position_open_fp(remover, category_id, call.from_user.id, subcategory_id))
#     else:
#         await call.message.edit_caption("<b>🎁 Товары в данное время отсутствуют.</b>")
#         await call.answer("❗ Позиции были изменены или удалены")
#
#
# # Следующая страница позиций для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_position_nextp", state="*")
# async def user_purchase_position_next_page(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#     category_id = int(call.data.split(":")[2])
#     subcategory_id = int(call.data.split(":")[3])
#
#
#     await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                  reply_markup=products_item_position_next_page_fp(remover, category_id, subcategory_id))
#
#
# # Предыдущая страница позиций для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_position_backp", state="*")
# async def user_purchase_position_prev_page(call: CallbackQuery, state: FSMContext):
#     remover = int(call.data.split(":")[1])
#     category_id = int(call.data.split(":")[2])
#     subcategory_id = int(call.data.split(":")[3])
#
#
#     await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                  reply_markup=buy_position_return_page_fp(remover, category_id, subcategory_id))
#
#
#
# ########################################### ПОКУПКА ##########################################
# # Выбор количества товаров для покупки
# @dp.callback_query_handler( IsChat(), text_startswith="buy_item_select", state="*")
# async def user_purchase_select(call: CallbackQuery, state: FSMContext):
#     position_id = int(call.data.split(":")[1])
#     settings = get_settingsx()
#
#     get_position = get_positionx(position_id=position_id)
#     get_items = get_itemsx(position_id=position_id)
#     get_user = get_userx(user_id=call.from_user.id)
#     if get_user['user_role'] == "VIP" and get_user['is_reseller'] == False:
#         get_position['position_price'] = int(get_position['position_price'] * (100- settings['vip_percent']) * 0.01)
#     elif get_user['user_role'] == "VIP" and get_user['is_reseller'] == True:
#         settings = get_settingsx()
#         get_position['position_price'] = int(get_position['position_price'] * (
#                 100 - settings['vip_percent'] - 15) * 0.01)
#     elif get_user['user_role'] == "Re-Seller":
#         get_position['position_price'] = int(get_position['position_price'] * (
#                 100 - 15) * 0.01)
#     if get_position['position_price'] != 0:
#         get_count = int(get_user['user_balance'] / get_position['position_price'])
#         if get_count > len(get_items): get_count = len(get_items)
#     else:
#         get_count = len(get_items)
#
#     if int(get_user['user_balance']) >= int(get_position['position_price']):
#         if get_count == 1:
#             await state.update_data(here_cache_position_id=position_id)
#             await state.finish()
#
#             await call.message.delete()
#             await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
#                                       f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
#                                       f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
#                                       f"🆔 Количество: <code>1шт</code>\n"
#                                       f"💳 Сумма к покупке: <code>{get_position['position_price']}₽</code>",
#                                       reply_markup=products_confirm_finl(position_id, 1))
#         elif get_count >= 1:
#             await state.update_data(here_cache_position_id=position_id)
#             await state.set_state("here_item_count")
#
#             await call.message.delete()
#             await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=f"<b>🎁 Введите количество товаров для покупки</b>\n"
#                                       f"▶ От <code>1</code> до <code>{get_count}</code>\n"
#                                       f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
#                                       f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n"
#                                       f"💳 Ваш баланс: <code>{get_user['user_balance']}₽</code>")
#         else:
#             await call.answer("🎁 Товаров нет в наличии")
#     else:
#         await call.answer("❗ У вас недостаточно средств. Пополните баланс", True)
#
#
# @dp.callback_query_handler( IsChat(), IsAdmin(), IsChat() ,text_startswith="show_item_select", state="*")
# async def user_purchase_select(call: CallbackQuery, state: FSMContext):
#     position_id = int(call.data.split(":")[1])
#     category_id = int(call.data.split(":")[2])
#     subcategory_id = int(call.data.split(":")[3])
#     items = get_itemsx(position_id=position_id)
#     get_category = get_categoryx(category_id=category_id)
#     get_subcategory = get_subcategoryx(subcategory_id=subcategory_id)
#
#
#
#     if items != []:
#         get_position = get_positionx(position_id=position_id)
#         get_items = get_itemsx(position_id=position_id)
#         text = "🎁 Изменение товара: \n" \
#                "—————————————————\n" \
#                f"🆕 Название: <code>{get_position['position_name']}</code>\n" \
#                f"🗃 Категория: <code>{get_category['category_name']}</code>\n"
#         if get_subcategory is not None:
#             text += f"📘 Подкатегория: <code>{get_subcategory['subcategory_name']}</code>\n"
#         text +=f"💳 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
#                f"🆔 Список ID:\n"
#         c = 1
#         more_media = {1: types.MediaGroup(), 2: types.MediaGroup(), 3: types.MediaGroup(), 4: types.MediaGroup(), 5: types.MediaGroup()}
#         k = 1
#         for item in items:
#             text += f"{c}. {item['item_data']} | <code>{item['item_id']}</code>\n"
#             c += 1
#             if os.path.isfile(f"tgbot/data/items/{item['item_data']}"):
#                 if len(more_media[5].media) == 10:
#                     continue
#                 more_media[k].attach_document(open(f"tgbot/data/items/{item['item_data']}", 'rb'), item['item_data'])
#                 if len(more_media[k].media) == 10:
#                     k += 1
#         is_file = False
#         for v in more_media.values():
#             if len(v.media) > 0:
#                 await bot.send_media_group(call.from_user.id, media=v)
#                 is_file = True
#         if not is_file:
#             try:
#                 await call.message.edit_caption(caption=text, reply_markup=user_edit_item(position_id, 0, category_id, subcategory_id=subcategory_id))
#             except:
#                 await call.message.delete()
#                 await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=text, reply_markup=user_edit_item(position_id, 0, category_id, subcategory_id))
#         else:
#             await call.message.delete()
#             await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=text,
#                                             reply_markup=user_edit_item(position_id, 0, category_id, subcategory_id))
#
#
#
#     else:
#         await call.answer("Товара нету.")
#
#
#
# @dp.callback_query_handler( IsChat(), IsAdmin(), IsChat(), text_startswith="change_item_select", state="*")
# async def user_purchase_select_change(call: CallbackQuery, state: FSMContext):
#     await state.finish()
#     position_id = int(call.data.split(":")[1])
#     category_id = int(call.data.split(":")[2])
#     if not get_itemsx(position_id=position_id) == []:
#         # await state.set_state(here_change_position_id=position_id)
#         # await state.set_state(here_change_category_id=category_id)
#         await state.set_state("here_change_item_select")
#         await call.message.answer("🎁 Введите id товара:")
#     else:
#         await call.message.answer("Товара нету.")
#
#
# @dp.message_handler( IsChat(), state="here_change_item_select")
# async def user_purchase_select_count(message: Message, state: FSMContext):
#     if message.text.isdigit():
#         if int(message.text) in get_all_items_id():
#             await state.update_data(here_change_item_select=int(message.text))
#             item = get_itemx(item_id=int(message.text))['item_data']
#             if os.path.isfile(f"tgbot/data/items/{item}"):
#                 await state.set_state("here_change_item_check_file")
#             else:
#                 await state.set_state("here_change_item_check")
#             await message.answer("🎁 Добавьте  товар:")
#         else:
#             await message.answer("Неверный id!")
#     else:
#         await message.answer("Ввод только числа!")
#
#
#
# @dp.message_handler( IsChat(), state="here_change_item_check")
# async def user_purchase_select_count(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         item_id = data['here_change_item_select']
#     item = get_itemsx(item_id=int(item_id))[0]
#     await state.update_data(here_new_item=message.text)
#     await message.answer("🆔 Вы действительно хотите изменить этот товар?", reply_markup=products_item_check(item_id, position_id=item['position_id'], category_id=item['category_id'], subcategory_id=item['subcategory_id']))
#
# @dp.message_handler( IsChat(), state="here_change_item_check_file", content_types=ContentType.DOCUMENT)
# async def user_purchase_select_count(message: Message, state: FSMContext):
#     async with state.proxy() as data:
#         item_id = data['here_change_item_select']
#     item = get_itemsx(item_id=int(item_id))[0]
#     await state.update_data(here_new_item=message.document)
#     await message.answer("🆔 Вы действительно хотите изменить этот товар?", reply_markup=products_item_check_file(item_id, position_id=item['position_id'], category_id=item['category_id'], subcategory_id=item['subcategory_id']))
#
# @dp.message_handler( IsChat(), state="here_change_item_check_file")
# async def user_purchase_select_count(message: Message, state: FSMContext):
#     await message.answer("Отправьте пожалуйста файл")
#
#
# @dp.callback_query_handler( IsChat(), IsAdmin(), IsChat(), text_startswith="change_item_file_check", state="*")
# async def user_purchase_jlhh(call: CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         file = data['here_new_item']
#     item_id = call.data.split(":")[1]
#     try:
#         item = get_itemx(item_id=item_id)
#         file_info = await bot.get_file(file.file_id)
#         if os.path.isfile(f"tgbot/data/items/{item['item_data']}"):
#             os.remove(f"tgbot/data/items/{item['item_data']}")
#         end = file.file_name.split(".")[-1]
#         item_data = str(random.randint(1000000000, 9999999999)) + "." + end
#         await bot.download_file(file_info.file_path, f'tgbot/data/items/{item_data}')
#         update_itemx(item_id=item_id, item_data=item_data)
#         await call.message.delete()
#         await call.message.answer("🎁 Товар был успешно изменен!")
#         position_id = int(call.data.split(":")[3])
#         category_id = int(call.data.split(":")[4])
#         subcategory_id = int(call.data.split(":")[5])
#         items = get_itemsx(position_id=position_id)
#         get_category = get_categoryx(category_id=category_id)
#         get_subcategory = get_subcategoryx(subcategory_id=subcategory_id)
#         if items != []:
#             get_position = get_positionx(position_id=position_id)
#             get_items = get_itemsx(position_id=position_id)
#             text = "🎁 Изменение товара: \n" \
#                    "—————————————————\n" \
#                    f"🆕 Название: <code>{get_position['position_name']}</code>\n" \
#                    f"🗃 Категория: <code>{get_category['category_name']}</code>\n"
#             if get_subcategory is not None:
#                 text += f"📘 Подкатегория: <code>{get_subcategory['subcategory_name']}</code>\n"
#             text += f"💳 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
#                     f"🆔 Список ID:\n"
#             c = 1
#             for item in items:
#                 text += f"{c}. {item['item_data']} | <code>{item['item_id']}</code>\n"
#                 c += 1
#             await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=text,
#                                             reply_markup=user_edit_item(position_id, 0, category_id, subcategory_id))
#     except:
#         await call.message.answer("Ошибка при изменении(")
#
#
#
# @dp.callback_query_handler( IsChat(), IsAdmin(), IsChat(), text_startswith="change_item_check", state="*")
# async def user_purchase_jlhh(call: CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         text = data['here_new_item']
#     item_id = call.data.split(":")[1]
#     # text = call.data.split(":")[2]
#     try:
#         update_itemx(item_id=item_id, item_data=text)
#         await call.message.delete()
#         await call.message.answer("🎁 Товар был успешно изменен!")
#         position_id = int(call.data.split(":")[3])
#         category_id = int(call.data.split(":")[4])
#         subcategory_id = int(call.data.split(":")[5])
#         items = get_itemsx(position_id=position_id)
#         get_category = get_categoryx(category_id=category_id)
#         get_subcategory = get_subcategoryx(subcategory_id=subcategory_id)
#         if items != []:
#             get_position = get_positionx(position_id=position_id)
#             get_items = get_itemsx(position_id=position_id)
#             text = "🎁 Изменение товара: \n" \
#                    "—————————————————\n" \
#                    f"🆕 Название: <code>{get_position['position_name']}</code>\n" \
#                    f"🗃 Категория: <code>{get_category['category_name']}</code>\n"
#             if get_subcategory is not None:
#                 text += f"📘 Подкатегория: <code>{get_subcategory['subcategory_name']}</code>\n"
#             text +=f"💳 Стоимость: <code>{get_position['position_price']}₽</code>\n" \
#                    f"🆔 Список ID:\n"
#             c = 1
#             for item in items:
#                 text += f"{c}. {item['item_data']} | <code>{item['item_id']}</code>\n"
#                 c += 1
#             await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=text,
#                                             reply_markup=user_edit_item(position_id, 0, category_id, subcategory_id))
#
#         else:
#             await call.message.answer("Товара нету.")
#
#     except:
#         await call.message.answer("Ошибка при изменении(")
#
#
#
#
# # Принятие количества товаров для покупки
# @dp.message_handler( IsChat(), state="here_item_count")
# async def user_purchase_select_count(message: Message, state: FSMContext):
#     position_id = (await state.get_data())['here_cache_position_id']
#     settings = get_settingsx()
#
#     get_position = get_positionx(position_id=position_id)
#     get_user = get_userx(user_id=message.from_user.id)
#     get_items = get_itemsx(position_id=position_id)
#     if get_user['user_role'] == "VIP" and get_user['is_reseller'] == False:
#         get_position['position_price'] = int(get_position['position_price'] * (100- settings['vip_percent']) * 0.01)
#     elif get_user['user_role'] == "VIP" and get_user['is_reseller'] == True:
#         settings = get_settingsx()
#         get_position['position_price'] = int(get_position['position_price'] * (
#                 100 - settings['vip_percent'] - 15) * 0.01)
#     elif get_user['user_role'] == "Re-Seller":
#         get_position['position_price'] = int(get_position['position_price'] * (
#                 100 - 15) * 0.01)
#     if get_position['position_price'] != 0:
#         get_count = int(get_user['user_balance'] / get_position['position_price'])
#         if get_count > len(get_items): get_count = len(get_items)
#     else:
#         get_count = len(get_items)
#
#     send_message = f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
#                    f"🎁 Введите количество товаров для покупки\n" \
#                    f"▶ От <code>1</code> до <code>{get_count}</code>\n" \
#                    f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n" \
#                    f"🎁 Товар: <code>{get_position['position_name']}</code> - <code>{get_position['position_price']}₽</code>\n" \
#                    f"💳 Ваш баланс: <code>{get_user['user_balance']}₽</code>"
#
#     if message.text.isdigit():
#         get_count = int(message.text)
#         print(get_position['position_price'])
#         amount_pay = int(get_position['position_price'] * get_count)
#
#         if len(get_items) >= 1:
#             if 1 <= get_count <= len(get_items):
#                 if int(get_user['user_balance']) >= amount_pay:
#                     await state.finish()
#                     await message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=f"<b>🎁 Вы действительно хотите купить товар(ы)?</b>\n"
#                                          f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
#                                          f"🎁 Товар: <code>{get_position['position_name']}</code>\n"
#                                          f"🆔 Количество: <code>{get_count}шт</code>\n"
#                                          f"💳 Сумма к покупке: <code>{amount_pay}₽</code>",
#                                          reply_markup=products_confirm_finl(position_id, get_count))
#                 else:
#                     await message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=f"<b>❌ Недостаточно средств на счете.</b>\n" + send_message)
#             else:
#                 await message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=f"<b>❌ Неверное количество товаров.</b>\n" + send_message)
#         else:
#             await state.finish()
#             await message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption="<b>🎁 Товар который вы хотели купить, закончился</b>")
#     else:
#         await message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption=f"<b>❌ Данные были введены неверно.</b>\n" + send_message)
#
#
# # Подтверждение покупки товара
# @dp.callback_query_handler( IsChat(), text_startswith="xbuy_item", state="*")
# async def user_purchase_confirm(call: CallbackQuery, state: FSMContext):
#     get_action = call.data.split(":")[1]
#     position_id = int(call.data.split(":")[2])
#     get_count = int(call.data.split(":")[3])
#
#     if get_action == "yes":
#         await call.message.edit_caption("<b>🔄 Ждите, товары подготавливаются</b>")
#
#         get_position = get_positionx(position_id=position_id)
#         get_items = get_itemsx(position_id=position_id)
#         get_user = get_userx(user_id=call.from_user.id)
#         settings = get_settingsx()
#         if get_user['user_role'] == "VIP" and get_user['is_reseller'] == False:
#             get_position['position_price'] = int(get_position['position_price'] * (100- settings['vip_percent']) * 0.01)
#         elif get_user['user_role'] == "VIP" and get_user['is_reseller'] == True:
#             settings = get_settingsx()
#             get_position['position_price'] = int(get_position['position_price'] * (
#                     100 - settings['vip_percent'] - 15) * 0.01)
#         elif get_user['user_role'] == "Re-Seller":
#             get_position['position_price'] = int(get_position['position_price'] * (
#                     100 - 15) * 0.01)
#         amount_pay = int(get_position['position_price'] * get_count)
#
#         if 1 <= int(get_count) <= len(get_items):
#             if int(get_user['user_balance']) >= amount_pay:
#                 save_items, send_count, split_len = buy_itemx(get_items, get_count)
#
#                 if get_count != send_count:
#                     amount_pay = int(get_position['position_price'] * send_count)
#                     get_count = send_count
#
#                 receipt = get_unix()
#                 buy_time = get_date()
#
#                 await call.message.delete()
#                 await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'),
#                                                 caption=f"<b>✅ Вы успешно купили товар(ы)</b>\n"
#                                                         f"➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
#                                                         f"🧾 Чек: <code>#{receipt}</code>\n"
#                                                         f"🎁 Товар: <code>{get_position['position_name']} | {get_count}шт | {amount_pay}₽</code>\n"
#                                                         f"🕰 Дата покупки: <code>{buy_time}</code>",
#                                                 reply_markup=menu_frep(call.from_user.id))
#                 if split_len == 0:
#                     await call.message.answer("🎁 Ваши товары:\n"+ "\n\n".join(save_items), parse_mode="None")
#                     try:
#                         for item in save_items:
#                             if os.path.isfile(f"tgbot/data/items/{item}"):
#                                 await bot.send_document(call.from_user.id, open(f"tgbot/data/items/{item}", 'rb'))
#                     except:
#                         pass
#                 else:
#                     for item in split_messages(save_items, split_len):
#                         await call.message.answer("🎁 Ваши товары:\n"+"\n\n".join(item), parse_mode="None")
#                         await asyncio.sleep(0.3)
#                         try:
#                             for item1 in item:
#                                 item1 = item1.split()[1]
#                                 if os.path.isfile(f"tgbot/data/items/{item1}"):
#                                     print("gggg")
#                                     await bot.send_document(call.from_user.id, open(f"tgbot/data/items/{item1}", 'rb'))
#                         except:
#                             pass
#
#                 update_userx(get_user['user_id'], user_balance=get_user['user_balance'] - amount_pay)
#                 add_purchasex(get_user['user_id'], get_user['user_login'], get_user['user_name'], receipt, get_count,
#                               amount_pay, get_position['position_price'], get_position['position_id'],
#                               get_position['position_name'], "\n".join(save_items), buy_time, receipt,
#                               get_user['user_balance'], int(get_user['user_balance'] - amount_pay))
#
#
#                 if get_user['user_role'] != "VIP" and get_user['user_role'] != "Admin" and get_user['user_role'] != "Buyer" and get_user['user_role'] != "Support" and get_user['user_role'] != "Re-Seller":
#                     update_userx(user_id=get_user['user_id'], user_role='Buyer')
#
#
#
#             else:
#                 await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption="<b>❗ На вашем счёте недостаточно средств</b>")
#         else:
#             await call.message.answer_photo(open('tgbot/data/resourses/photo/buy.jpg', 'rb'), caption="<b>🎁 Товар который вы хотели купить закончился или изменился.</b>",
#                                       reply_markup=menu_frep(call.from_user.id))
#     else:
#         if len(get_all_categoriesx()) >= 1:
#             await call.message.edit_caption("<b>🎁 Выберите нужный вам товар:</b>",
#                                          reply_markup=products_item_category_open_fp(0))
#         else:
#             await call.message.edit_caption("<b>✅ Вы отменили покупку товаров.</b>")
