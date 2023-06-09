import datetime
import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from misc.states import UserState
from utils.misc.kb_config import users_list_btn, find_user_btn, back_btn


async def users_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    inline_keyboard = [
        [InlineKeyboardButton(text=users_list_btn, callback_data=f"users_list:0")],
         [InlineKeyboardButton(text=find_user_btn, callback_data=f"find_user")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.answer("Выберите опцию", reply_markup=keyboard)


async def find_user_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):

    await call.message.edit_text("Введите ID пользователя:")
    await state.set_state(UserState.user_id)


async def get_user_handler(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    user_id = message.text
    user_db = await DBCommands(User, session).get(user_id=user_id)
    if user_db != None:
        # text = profile_text.format(user_db.user_id, user_db.balance, user_db.token_count, user_db.total_balance)

        # date_object = datetime.datetime.strptime(user_db.registration_time, '%Y-%m-%d %H:%M:%S.%f')
        # Форматируем дату в нужном формате
        formatted_date = user_db.registration_time.strftime('%d.%m.%Y')
        if user_db.referrer_id is not None:
            referrer = await DBCommands(User, session).get(user_id=user_db.referrer_id)
            text = f"🆔 ID: {user_db.user_id}\n" \
                   f"👤 Логин: @{user_db.user_name}\n" \
                   f"⏰ Регистрация: {formatted_date}\n" \
                   f"💳 Баланс: {user_db.balance}₽\n" \
                   f"🪪 Пригласил: @{referrer.user_name}\n" \
                   f"👥 Приглашенных: {user_db.referrer_count}\n"
        else:
            text = f"🆔 ID: {user_db.user_id}\n" \
                   f"👤 Логин: @{user_db.user_name}\n" \
                   f"⏰ Регистрация: {formatted_date}\n" \
                   f"💳 Баланс: {user_db.balance}₽\n" \
                   f"👥 Приглашенных: {user_db.referrer_count}\n"
        if user_db.time_to_action is not None:
            if user_db.time_to_action > datetime.datetime.now():
                formatted_date2 = user_db.time_to_action.strftime('%d.%m.%Y')
                text += f"✅ Оплачен до: {formatted_date2}\n"
            else:
                text += f"❌ Не оплачено\n"
        else:
            text += f"❌ Не оплачено\n"
        await message.answer(text)
    else:
        await message.answer("Пользователь не найден!")



async def get_users_list_inl(session, page=0):
    max_len = 5
    c = 0
    keyboard = []
    users = await DBCommands(User, session).get(_first=False)

    for i in range(page, len(users)):
        if c == max_len:
            break
        keyboard.append([InlineKeyboardButton(text=f"{users[i].user_name} {users[i].user_id}", callback_data=f"show_user_detail:{users[i].user_id}:{page}")])
        c += 1

    if max_len < len(users) and page == 0:
        keyboard.append([InlineKeyboardButton(text="Дальше", callback_data=f"users_list:{page+max_len}")])
    elif max_len + page < len(users) and page != 0:
        keyboard.append([InlineKeyboardButton(text="Назад", callback_data=f"users_list:{page-max_len}"),
                     InlineKeyboardButton(text="Дальше", callback_data=f"users_list:{page+max_len}")])
    else:
        if page == 0:
            pass
        else:
            keyboard.append([InlineKeyboardButton(text="Назад", callback_data=f"users_list:{page-max_len}")])
    inl_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    return inl_keyboard

async def users_list_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    page = int(call.data.split(":")[1])
    if page < 0:
        page = 0
    await call.message.edit_text("Пользователи", reply_markup=await get_users_list_inl(session, page))


async def select_user_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    user_id = int(call.data.split(":")[1])
    page = int(call.data.split(":")[2])
    user_db = await DBCommands(User, session).get(user_id=user_id)
    # text = profile_text.format(user_db.user_id, user_db.balance, user_db.token_count, user_db.total_balance)

    # date_object = datetime.datetime.strptime(user_db.registration_time, '%Y-%m-%d %H:%M:%S.%f')

    # Форматируем дату в нужном формате
    formatted_date = user_db.registration_time.strftime('%d.%m.%Y')
    if user_db.referrer_id is not None:
        referrer = await DBCommands(User, session).get(user_id=user_db.referrer_id)
        text = f"🆔 ID: {user_db.user_id}\n" \
               f"👤 Логин: @{user_db.user_name}\n" \
               f"⏰ Регистрация: {formatted_date}\n" \
               f"💳 Баланс: {user_db.balance}₽\n" \
               f"🪪 Вас Пригласил: @{referrer.user_name}\n" \
               f"👥 Приглашенных: {user_db.referrer_count}\n"
    else:
        text = f"🆔 ID: {user_db.user_id}\n" \
               f"👤 Логин: @{user_db.user_name}\n" \
               f"⏰ Регистрация: {formatted_date}\n" \
               f"💳 Баланс: {user_db.balance}₽\n" \
               f"👥 Приглашенных: {user_db.referrer_count}\n"
    if user_db.time_to_action is not None:
        if user_db.time_to_action > datetime.datetime.now():
            formatted_date2 = user_db.time_to_action.strftime('%d.%m.%Y')
            text += f"✅ Оплачен до: {formatted_date2}\n"
        else:
            text += f"❌ Не оплачено\n"
    else:
        text += f"❌ Не оплачено\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=back_btn, callback_data=f"users_list:{page}")]])
    await call.message.edit_text(text, reply_markup=keyboard)