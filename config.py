from dataclasses import dataclass

from environs import Env

from database.models.user import User


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Finances:
    min_withdraw_sum: int
    max_withdraw_sum: int



@dataclass
class Config:
    tg_bot: TgBot
    finances: Finances


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS")))
        ),
        finances=Finances(min_withdraw_sum=env.int("MIN_WITHDRAW_SUM"),
                          max_withdraw_sum=env.int("MAX_WITHDRAW_SUM")
        ),

    )


TABLES = {'users': User}
