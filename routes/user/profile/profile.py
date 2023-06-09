import datetime
from typing import Union, List

from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMedia, InputMediaPhoto, InlineKeyboardButton, \
    InlineKeyboardMarkup, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.user import User
from utils.misc.kb_config import withdraw_money_btn, refill_btn


async def back_to_profile_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()

    await profile_handler(call, state, session)


async def profile_handler(upd: Union[Message, CallbackQuery], state: FSMContext, session: AsyncSession, bot: Bot):
    await state.clear()

    user_id = upd.from_user.id
    message = upd if isinstance(upd, Message) else upd.message

    user_db = await DBCommands(User, session).get(user_id=user_id)

    # date_object = datetime.datetime.strptime(user_db.registration_time, '%Y-%m-%d %H:%M:%S.%f')

    # Форматируем дату в нужном формате
    formatted_date = user_db.registration_time.strftime('%d.%m.%Y')
    if user_db.referrer_id is not None:
        referrer = await DBCommands(User, session).get(user_id=user_db.referrer_id)
        text = f"🆔 Ваш ID: {user_db.user_id}\n" \
              f"👤 Ваш Логин: @{user_db.user_name}\n" \
              f"⏰ Регистрация: {formatted_date}\n" \
              f"💳 Ваш Баланс: {user_db.balance}₽\n" \
              f"🪪 Вас Пригласил: @{referrer.user_name}\n" \
              f"👥 У Вас приглашенных: {user_db.referrer_count}\n"
    else:
        text = f"🆔 Ваш ID: {user_db.user_id}\n" \
               f"👤 Ваш Логин: @{user_db.user_name}\n" \
               f"⏰ Регистрация: {formatted_date}\n" \
               f"💳 Ваш Баланс: {user_db.balance}₽\n" \
               f"👥 У Вас приглашенных: {user_db.referrer_count}\n"
    if user_db.time_to_action is not None:
        if user_db.time_to_action > datetime.datetime.now():
            formatted_date2 = user_db.time_to_action.strftime('%d.%m.%Y')
            text += f"✅ Оплачен до: {formatted_date2}\n"
            link = 'https://t.me/' + str((await bot.me()).username) + '?start=' + str(message.from_user.id)
            text += "🔗 Ваша пригласительная ссылка:\n\n" \
                    f"<code>{link}</code>"
        else:
            text += f"❌ Не оплачено\n"
    else:
        text += f"❌ Не оплачено\n"

    # text = f"ID: {user_db.user_id}\n" \
    #        f"@{user_db.user_name}\n" \
    #        f"Registration: {user_db.registration_time}\n" \
    #        f"Баланс: {user_db.balance}₽\n" \
    #        f"Refill: {user_db.refill_count}\n" \
    #        f"Refill_from_referrer: {user_db.refill_from_referrer}\n" \
    #        f"Referrer count: {user_db.referrer_count}\n" \
    #        f"Action_date: {user_db.time_to_action}\n"
    inline_keyboard = [
        # [InlineKeyboardButton(text=refill_btn, callback_data=f"refill_money"),
        #  ],
        [InlineKeyboardButton(text=withdraw_money_btn, callback_data=f"withdraw_money"),
         ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    img = FSInputFile('./images/profile_img.jpg')
    if isinstance(upd, CallbackQuery):
        await message.edit_caption(caption=text, reply_markup=keyboard)
    else:
        await message.answer_photo(img, caption=text, reply_markup=keyboard)



