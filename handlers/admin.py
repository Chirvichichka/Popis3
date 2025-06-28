from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import Config

router = Router()

@router.message(Command("set_time"))
async def set_time_command(message: Message, config: Config):
    time_variants = ["short", "medium", "long", "very long", "very very long"]
    time = message.text.replace("/set_time ", "")

    chat_id = message.chat.id

    chat_settings = config.chat_settings

    if time in time_variants:
        if not chat_settings.get(str(chat_id)):
            chat_settings[str(chat_id)] = {}

        chat_settings[str(chat_id)]["popis_rave_wait"] = time

        config.upload_chat_settings(chat_settings)

        await message.answer(f"Изменил время на {time}")
    else:
        await message.answer("Нет такого")