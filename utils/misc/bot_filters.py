# - *- coding: utf- 8 - *-
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from services.dbhandler import isBan, get_req


class IsChat(BoundFilter):
    async def check(self, message: types.Message):
        if message.chat.id > 0:
            return True
        else:
            return False


class IsNoBan(BoundFilter):
    async def check(self, message: types.Message):
        isban_db = isBan(message.from_user.id)
        isban_req = get_req(user_id=message.from_user.id)
        if isban_db is not None:
            if not isban_db:
                if isban_req is None:
                    return True
                elif isban_req['status'] == 'Ban':
                    return False
                else:
                    return True
            else:
                return False
        else:
            if isban_req is None:
                return True
            elif isban_req['status'] == 'Ban':
                return False
            else:
                return True



