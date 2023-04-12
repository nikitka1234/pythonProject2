from aiogram import types, Dispatcher

from os import remove

from bot.create_bot import bot
from keyboards import client_kb

import bot.settings as settings


async def send_welcome(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\n\n")
    await message.answer(settings.HELP_MESSAGE, reply_markup=client_kb.client_kb)


async def send_help(message: types.Message):
    await message.answer(settings.HELP_MESSAGE, reply_markup=client_kb.client_kb)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_help, commands=['help'])

    dp.register_message_handler(send_help, lambda message: message.text == 'Помощь')
