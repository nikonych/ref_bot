from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


async def get_inline_kb():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="", callback_data=f""),
                 )
    return keyboard

def get_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("")
    return keyboard