from config import bot, dp, Staff
from aiogram import executor, types
import logging

from handlers import commands, fsm_store, send_products, fsm_order

from db import db_main



async def on_startup(_):
    for admin in Staff:
        await bot.send_message(chat_id=admin, text='Бот включен!')

        await db_main.sql_create()


async def on_shutdown(_):
    for admin in Staff:
        await bot.send_message(chat_id=admin, text='Бот выключен!')


commands.register_commands(dp)
fsm_order.reg_handler_fsm_order(dp)
fsm_store.reg_handler_fsm_store(dp)

send_products.register_handlers(dp)





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, allowed_updates=['callback'],
                           on_startup=on_startup, on_shutdown=on_shutdown)