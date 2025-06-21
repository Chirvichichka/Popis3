import asyncio
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from generation import NewsGenerator
from generation import QuoteGenerator

from keyboards import generation_text_keyboard