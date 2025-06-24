import random

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message

from generation import NewsGenerator
from generation import QuoteGenerator
from generation import RaveGenerator
from keyboards import generation_text_keyboard

router = Router()

commands = ["/start", "/commands", "/news", "/quote", "/rave", "/prob"]


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет, я попис-адептус, я пока не умею материться", reply_markup=generation_text_keyboard)


@router.message(Command("commands"))
async def commands_command(message: Message):
    await message.answer("\n".join(commands), reply_markup=generation_text_keyboard)


@router.message(Command("prob"))
async def prob_command(message: Message):
    await message.answer(f"Вероятность этого {random.randint(1, 99)}.{random.randint(1, 99):02}%")


@router.message(Command("rave"))
async def rave_command(message: Message, rave: RaveGenerator):
    await message.answer(rave.generate())


@router.message(Command("news"))
async def news_command(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, "typing")

    start_word = message.text.replace("/news ", "")

    news_generator = NewsGenerator()
    news = news_generator.generate(language="ru", start_word=start_word)

    await message.answer(news)


@router.message(Command("quote"))
async def quote_command(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, "typing")
    quote_generator = QuoteGenerator()
    quote = quote_generator.generate(language="ru")
    await message.answer(quote)


@router.message(F.text)
async def handle_text(message: Message, rave: RaveGenerator):
    rave.add_text(message.text.lower())
