from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import bot.settings as settings


API_TOKEN = settings.API_TOKEN
if not API_TOKEN:
    exit("Error: no token provided")


# Инициализируем бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
