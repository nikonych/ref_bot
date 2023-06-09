import json
from datetime import timedelta, datetime

from sqlalchemy import update, not_

from database.db_commands import DBCommands
from database.models.user import User


async def add_percent_to_users(session_pool):
    async with session_pool() as session:
        time_now = datetime.utcnow()
        settings = open("database/settings.json", "r")
        with settings as read_file:
            data = json.load(read_file)
        items = data["actions"]
        print("add_percent_to_users")
        users = await DBCommands(User, session).get(_first=False)
        for user in users:
            if user.time_to_action is not None:
                if user.time_to_action > time_now:
                    if user.action_type == 'day':
                        amount = 0.003 * float(items[0]['price'])
                    elif user.action_type == 'week':
                        amount = 0.003 * float(items[1]['price'])
                    else:
                        amount = 0.003 * float(items[2]['price'])
                    await DBCommands(User, session).update(values=dict(balance=user.balance + amount),
                                                           where=dict(user_id=user.user_id))
            # ref_users = await DBCommands(User, session).get(_first=False, referrer_id=user.user_id)
            # for ref in ref_users:
            #     if ref.time_to_action is not None:
            #         if ref.time_to_action > time_now:
            #             if ref.action_type == 'day':
            #                 amount = 0.15 * int(items[0]['price'])
            #             elif ref.action_type == 'week':
            #                 amount = 0.15 * int(items[1]['price'])
            #             else:
            #                 amount = 0.15 * int(items[2]['price'])
            #             await DBCommands(User, session).update(values=dict(balance=int(user.balance + amount)),
            #                                                    where=dict(user_id=user.user_id))

        await session.commit()
