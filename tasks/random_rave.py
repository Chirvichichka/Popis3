import asyncio
import random

from aiogram import Bot

from config import Config
from generation.rave.rave_generator import RaveGenerator

def get_time(chat_id, config: Config):
    chat_settings = config.chat_settings
    time = chat_settings[str(chat_id)]["popis_rave_wait"]

    time_variants = {
        "short": (30, 120),
        "medium": (60, 300),
        "long": (60, 900),
        "very long": (60, 1800),
    }

    return random.randint(*time_variants[time])


async def send_random_rave(bot: Bot, chat_id: int, rave: RaveGenerator, config: Config):
    while True:
        wait_time = get_time(chat_id, config)
        text = rave.generate()

        await asyncio.sleep(wait_time)
        await bot.send_message(chat_id=chat_id, text=text)
