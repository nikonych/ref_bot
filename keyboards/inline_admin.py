from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def accept_user_inl(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🟢 Принять", callback_data=f"accept_user:True:{user_id}"),
                 InlineKeyboardButton(text="🔴 Отклонить", callback_data=f"accept_user:False:{user_id}"))


    return keyboard


async def get_balance(user_id, data):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="✅ Добавить баланс", callback_data=f"addbalance:{user_id}:{data}"),
                 InlineKeyboardButton(text="❌ Пусто", callback_data=f"empty:{user_id}:{data}"))

    print(keyboard)
    return keyboard

async def kick_user_inl(user_id):
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="❌ Выгнать", callback_data=f"accept_user:Ban:{user_id}"))
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="↪️ Вернуть в команду", callback_data=f"accept_user:ReAdd:{user_id}"))

    return keyboard

async def reAdd_user_inl(user_id):
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="↪️ Вернуть в команду", callback_data=f"accept_user:ReAdd:{user_id}"))
    return keyboard