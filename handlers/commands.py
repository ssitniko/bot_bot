from aiogram import types, Dispatcher
from config import bot, dp
import os



async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}\n')


async def info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'bot_bot предназначен для заказа товаров\n'
                            f'Команды бота:\n'
                            f'* /products - для просмотра товаров\n'
                            f'* /order - для заказа товаров\n')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(info, commands=['info'])


