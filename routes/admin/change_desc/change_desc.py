from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession
from utils.misc.kb_config import change_rule_url_btn, change_rule_img_btn, change_rule_text_btn, change_help_img_btn, change_help_text_btn, change_help_user_btn, change_main_img_btn, change_main_text_btn

async def change_desc_handler(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    inline_keyboard = [
        [InlineKeyboardButton(text=change_main_img_btn, callback_data=f"change_img:main"), InlineKeyboardButton(text=change_main_text_btn, callback_data=f"change_text:main")],
        [InlineKeyboardButton(text=change_help_img_btn, callback_data=f"change_img:help"), InlineKeyboardButton(text=change_help_text_btn, callback_data=f"change_text:help")],
        [InlineKeyboardButton(text=change_rule_img_btn, callback_data=f"change_img:rule"), InlineKeyboardButton(text=change_rule_text_btn, callback_data=f"change_text:rule")],
        [InlineKeyboardButton(text=change_help_user_btn, callback_data=f"change_url:user"), InlineKeyboardButton(text=change_rule_url_btn, callback_data=f"change_url:rule")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await message.answer(".", reply_markup=keyboard)
