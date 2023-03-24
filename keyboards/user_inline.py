from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.kb_config import *


def get_check_token_type_inl():
    keyboard = InlineKeyboardMarkup()
    keyboard.inline_keyboard =[[InlineKeyboardButton(text=full_info_btn, callback_data=f"send_txt:yes")],
                 [InlineKeyboardButton(text=no_info_btn, callback_data=f"send_txt:no")]]
    return keyboard


def get_check_file_inl(check_type, user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=add_money_btn, callback_data=f"add_money:{user_id}:{check_type}"),
                 InlineKeyboardButton(text=empty_btn, callback_data=f"empty:{user_id}:{check_type}")
                 )
    if check_type == "yes":
        keyboard.add(InlineKeyboardButton(text=send_proof_btn, callback_data=f"send_proof:{user_id}:{check_type}"))
    return keyboard


def get_are_you_sure_inl(user_id, check_type):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=yes_btn, callback_data=f"sure:yes:{user_id}:{check_type}"),
                 InlineKeyboardButton(text=no_btn, callback_data=f"sure:no:{user_id}:{check_type}")
                 )
    return keyboard