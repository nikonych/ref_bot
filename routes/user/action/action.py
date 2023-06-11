import json
from datetime import datetime, timedelta, date

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_commands import DBCommands
from database.models.refill import Refill
from database.models.user import User
from utils.misc.kb_config import qiwi_btn, lolz_btn, lava_btn
from utils.payments import lava
from utils.payments.lzt import Lolz
from utils.payments.qiwi import QiwiAPI
from utils.payments.yooMoney import YooMoneyAPI


async def get_actions_type_handler(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()

    inline_keyboard = [[InlineKeyboardButton(text="Оплатить", callback_data="refill_type:yoomoney")]]
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    # for i in range(len(data["actions"])):
    #     item = data["actions"][i]
    #     inline_keyboard.append(
    #         [InlineKeyboardButton(text=item['name'], callback_data=f"action_type:{i}:{item['duration']}"),
    #          ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await message.answer(data['action_text'], reply_markup=keyboard)


async def chose_refill_type_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    inline_keyboard = [
        [InlineKeyboardButton(text=lava_btn, callback_data=f"refill_type:lava"),
         ],
        # [InlineKeyboardButton(text=lolz_btn, callback_data=f"refill_type:lolz"),
        #  ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await call.message.edit_text("Выберите тип пополнения:", reply_markup=keyboard)


async def get_refill_count_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    refill_type = call.data.split(":")[1]
    if refill_type == 'qiwi':
        get_message, get_link, receipt = await (
            await QiwiAPI()
        ).bill_pay(200)
    elif refill_type == 'lava':
        # get_message, get_link, receipt = await lava.bill_pay(200)
        # await state.update_data(payment=get_link)
        # get_link = get_link.url
        get_link = "google.com"
        receipt = "gfdsgfdsgfdsgfds"
        get_message = "ggggg"
    elif refill_type == 'yoomoney':
        get_message, get_link, receipt = await (
            await YooMoneyAPI()
        ).bill_pay(200)
        await state.update_data(payment=get_link)
        print(get_message, get_link, receipt)
    else:
        lzt = await Lolz()
        receipt = lzt.get_random_string().split('.')[1]
        get_link, get_message = await lzt.get_link(200, receipt)

    inline_keyboard = [
        [InlineKeyboardButton(text="Оплатить", url=get_link),
         ],
        [InlineKeyboardButton(text="Проверить оплату", callback_data=f"check_pay:{refill_type}:{receipt}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await call.message.edit_text(get_message, reply_markup=keyboard)


async def check_pay_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    refill_type = call.data.split(":")[1]
    receipt = call.data.split(":")[2]
    # if refill_type == 'qiwi':
    #     pay_status, pay_amount = await (
    #         await QiwiAPI()
    #     ).check_form(receipt)
    #
    #     if pay_status == "PAID":
    #         user_db = await DBCommands(User, session).get(user_id=call.from_user.id)
    #         # await DBCommands(User, session).update(values=dict(balance=user_db.balance + pay_amount,
    #         #                                                    total_balance=
    #         #                                                        user_db.total_balance + pay_amount),
    #         #                                        where=dict(user_id=call.from_user.id))
    #         await DBCommands(Refill, session).add(user_id=call.from_user.id, refill_id=receipt, amount=pay_amount,
    #                                               refill_type=refill_type)
    #         if user_db.referrer_id is not None:
    #             referrer = await DBCommands(User, session).get(user_id=user_db.referrer_id)
    #             await DBCommands(User, session).update(values=dict(balance=referrer.balance + 100,
    #                                                                total_balance=
    #                                                                referrer.total_balance + 100,
    #                                                                refill_from_referrer=referrer.refill_from_referrer + 100),
    #                                                    where=dict(user_id=user_db.referrer_id))
    #             if not user_db.has_payed_before:
    #                 await bot.send_message(chat_id=user_db.referrer_id,
    #                                        text=f"🔗 У вас новый реферал: @{user_db.username}"
    #                                             f"💳 Вам начислено: 100р")
    #                 await DBCommands(User, session).update(values=dict(has_payed_before=True),
    #                                                        where=dict(user_id=call.from_user.id))
    #                 await DBCommands(User, session).update(values=dict(referrer_count=referrer.referrer_count + 1),
    #                                                        where=dict(user_id=user_db.referrer_id))
    #             else:
    #                 await bot.send_message(chat_id=user_db.referrer_id,
    #                                        text=f"🔗 От реферала: @{user_db.username}"
    #                                             f"💳 Вам начислено: 100р")
    #         await call.message.edit_reply_markup(None)
    #         # Получаем текущую дату
    #         сurrent_date = date.today()
    #
    #         # Добавляем 2 недели к текущей дате
    #         future_date = сurrent_date + timedelta(weeks=2)
    #
    #         await DBCommands(User, session).update(
    #             values=dict(time_to_action=future_date),
    #             where=dict(user_id=call.from_user.id))
    #         link = 'https://t.me/' + str((await bot.me()).username) + '?start=' + str(call.from_user.id)
    #         await call.message.edit_text("✅ Вы успешно оплатили доступ к пользованию ботом!\n"
    #                                      "🔗 Ваша персональная ссылка приглашения для заработка:\n"
    #                                      f"<code>{link}</code>")
    #     elif pay_status == "EXPIRED":
    #         await call.message.edit_text("<b>❌ Время оплаты вышло. Платёж был удалён.</b>")
    #     elif pay_status == "WAITING":
    #         await call.answer("❗ Платёж не был найден.\n"
    #                           "⌛ Попробуйте чуть позже.", True, cache_time=5)
    #     elif pay_status == "REJECTED":
    #         await call.message.edit_text("<b>❌ Счёт был отклонён.</b>")
    if refill_type == 'yoomoney':
        pay_status, pay_amount = await (
                    await YooMoneyAPI()
                ).check_pay(receipt)
        # pay_status, pay_amount = True, 100
        if pay_status:
            user_db = await DBCommands(User, session).get(user_id=call.from_user.id)
            # await DBCommands(User, session).update(values=dict(balance=user_db.balance + pay_amount,
            #                                                    total_balance=
            #                                                        user_db.total_balance + pay_amount),
            #                                        where=dict(user_id=call.from_user.id))
            await DBCommands(Refill, session).add(user_id=call.from_user.id, refill_id=receipt, amount=pay_amount,
                                                  refill_type=refill_type)
            if user_db.referrer_id is not None:
                referrer = await DBCommands(User, session).get(user_id=user_db.referrer_id)
                await DBCommands(User, session).update(values=dict(balance=referrer.balance + 100,
                                                                   total_balance=
                                                                   referrer.total_balance + 100,
                                                                   refill_from_referrer=referrer.refill_from_referrer + 100),
                                                       where=dict(user_id=user_db.referrer_id))
                if not user_db.has_payed_before:
                    await bot.send_message(chat_id=user_db.referrer_id,
                                           text=f"🔗 У вас новый реферал: @{user_db.user_name}\n"
                                                f"💳 Вам начислено: 100р")
                    await DBCommands(User, session).update(values=dict(has_payed_before=True),
                                                           where=dict(user_id=call.from_user.id))
                    await DBCommands(User, session).update(values=dict(referrer_count=referrer.referrer_count + 1),
                                                           where=dict(user_id=user_db.referrer_id))
                else:
                    await bot.send_message(chat_id=user_db.referrer_id,
                                           text=f"🔗 От реферала: @{user_db.user_name}\n"
                                                f"💳 Вам начислено: 100р")
            await call.message.edit_reply_markup(None)
            # Получаем текущую дату
            сurrent_date = date.today()

            # Добавляем 2 недели к текущей дате
            future_date = сurrent_date + timedelta(weeks=2)

            await DBCommands(User, session).update(
                values=dict(time_to_action=future_date),
                where=dict(user_id=call.from_user.id))
            link = 'https://t.me/' + str((await bot.me()).username) + '?start=' + str(call.from_user.id)
            await call.message.edit_text("✅ Вы успешно оплатили доступ к пользованию ботом!\n"
                                         "🔗 Ваша персональная ссылка приглашения для заработка:\n"
                                         f"<code>{link}</code>")
        else:
            await call.answer("❗ Платёж не был найден.\n"
                          "⌛ Попробуйте чуть позже.", True, cache_time=5)
    else:
        lolz = await Lolz()
        if lolz.check_payment(comment=receipt, amount=1) or True:
            user_db = await DBCommands(User, session).get(user_id=call.from_user.id)
            # await DBCommands(User, session).update(values=dict(balance=int(user_db.balance + 200),
            #                                                    total_balance=int(
            #                                                        user_db.total_balance + 200)),
            #                                        where=dict(user_id=call.from_user.id))
            await DBCommands(Refill, session).add(user_id=call.from_user.id, refill_id=receipt, amount=200,
                                                  refill_type=refill_type)
            if user_db.referrer_id is not None:
                referrer = await DBCommands(User, session).get(user_id=user_db.referrer_id)
                await DBCommands(User, session).update(values=dict(balance=referrer.balance + 100,
                                                                   total_balance=
                                                                   referrer.total_balance + 100,
                                                                   refill_from_referrer=referrer.refill_from_referrer + 100),
                                                       where=dict(user_id=user_db.referrer_id))
                if not user_db.has_payed_before:
                    await bot.send_message(chat_id=user_db.referrer_id,
                                           text=f"🔗 У вас новый реферал: @{user_db.user_name}\n"
                                                f"💳 Вам начислено: 100р")
                    await DBCommands(User, session).update(values=dict(has_payed_before=True),
                                                           where=dict(user_id=call.from_user.id))
                    await DBCommands(User, session).update(values=dict(referrer_count=referrer.referrer_count + 1),
                                                           where=dict(user_id=user_db.referrer_id))
                else:
                    await bot.send_message(chat_id=user_db.referrer_id,
                                           text=f"🔗 От реферала: @{user_db.user_name}\n"
                                                f"💳 Вам начислено: 100р")
            # Получаем текущую дату
            сurrent_date = date.today()

            # Добавляем 2 недели к текущей дате
            future_date = сurrent_date + timedelta(weeks=2)

            await DBCommands(User, session).update(
                values=dict(time_to_action=future_date),
                where=dict(user_id=call.from_user.id))
            link = 'https://t.me/' + str((await bot.me()).username) + '?start=' + str(call.from_user.id)
            await call.message.edit_text("✅ Вы успешно оплатили доступ к пользованию ботом!\n"
                                         "🔗 Ваша персональная ссылка приглашения для заработка:\n"
                                         f"<code>{link}</code>")

        else:
            await call.answer("❗ Платёж не был найден.\n"
                              "⌛ Попробуйте чуть позже.", True, cache_time=5)


async def get_action_detail_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    index = int(call.data.split(":")[1])
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    item = data["actions"][index]
    inline_keyboard = [
        [InlineKeyboardButton(text="Купить", callback_data=f"buy_action:{index}")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    await call.message.edit_text("Description:" + item["description"] + "\n"
                                                                        "Price:" + str(item["price"]) + "\n",
                                 reply_markup=keyboard)


async def buy_action_handler(call: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    index = int(call.data.split(":")[1])
    settings = open("database/settings.json", "r")
    with settings as read_file:
        data = json.load(read_file)
    item = data["actions"][index]
    user_db = await DBCommands(User, session).get(user_id=call.from_user.id)
    current_datetime = datetime.now()
    time_to_action = user_db.time_to_action
    if time_to_action is None:
        is_user_has_action = False
    else:
        is_user_has_action = current_datetime < time_to_action
    print(is_user_has_action)
    if user_db.balance >= item["price"] and is_user_has_action is False:
        price = int(item["price"])
        await DBCommands(User, session).update(values=dict(balance=int(user_db.balance - price)),
                                               where=dict(user_id=call.from_user.id))
        if item["duration"] == "day":
            current_datetime = datetime.now()
            next_day_datetime = current_datetime + timedelta(days=1)
        elif item["duration"] == "week":
            current_datetime = datetime.now()
            next_day_datetime = current_datetime + timedelta(days=7)
        else:
            current_datetime = datetime.now()
            next_day_datetime = current_datetime + timedelta(days=30)
        await DBCommands(User, session).update(
            values=dict(time_to_action=next_day_datetime, action_type=item['duration']),
            where=dict(user_id=call.from_user.id))
        link = 'https://t.me/' + str((await bot.me()).username) + '?start=' + str(call.from_user.id)
        await call.message.edit_text("Спасибо за покупку!\n"
                                     "Ваша реферальная ссылка:\n"
                                     f"<code>{link}</code>")
    elif is_user_has_action:
        await call.answer("У вас уже есть активная акция")
    else:
        await call.answer("Не хватает баланса")
