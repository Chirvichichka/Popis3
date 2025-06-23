import asyncio
import os
import random

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from generation import NewsGenerator
from generation import QuoteGenerator
from generation import RaveGenerator

from keyboards import generation_text_keyboard