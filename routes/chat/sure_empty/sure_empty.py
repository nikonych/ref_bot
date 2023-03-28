import json

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from misc.states import TokenState
from utils.misc.kb_config import add_money_btn, empty_btn, send_proof_btn


async def sure_empty_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    user_id = call.from_user.id
    check_type = call.data.split(":")[3]
    if call.data.split(":")[1] == 'no':
        inline_keyboard = [
            [InlineKeyboardButton(text=add_money_btn, callback_data=f"add_money:{user_id}:{check_type}"),
             InlineKeyboardButton(text=empty_btn, callback_data=f"empty:{user_id}:{check_type}")],
        ]
        if check_type == "yes":
            inline_keyboard.append(
                [InlineKeyboardButton(text=send_proof_btn, callback_data=f"send_proof:{user_id}:{check_type}")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await call.message.edit_caption(caption=call.message.caption.split("\n\n")[0],
                                        reply_markup=keyboard)
    else:
        if check_type == "no":
            await bot.send_message(chat_id=user_id, text="✅ Ваши токены успешно отработаны!\n"
                                                         "❌ К сожелению ваши токены оказались не валидными, или пустыми!")
            await call.message.edit_caption(caption=call.message.caption.split("\n\n")[0] + "\n"
                                                                                            "❌ Файл пустой")
        else:
            msg = await call.message.answer("📁 Прикрепите скриншот отчета отработки токенов!")
            await state.update_data(messages_id=[msg.message_id])
            await state.update_data(is_empty=True)
            await state.set_state(TokenState.proof)
