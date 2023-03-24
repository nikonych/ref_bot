from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.kb_config import *



def get_menu_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   keyboard=[
                                       [KeyboardButton(text=load_token_btn)],
                                       [KeyboardButton(text=profile_btn), KeyboardButton(text=rule_btn)],
                                       [KeyboardButton(text=help_btn)]
                                   ])

    return keyboard
