
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import db_main


async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_all = types.InlineKeyboardButton('Вывести все товары', callback_data='all')
    button_one = types.InlineKeyboardButton('Вывести по одному', callback_data='one')
    keyboard.add(button_all, button_one)

    await message.answer('Выберите как отправить товары:', reply_markup=keyboard)


async def send_all_products(callback_query: types.CallbackQuery):
    products = db_main.fetch_all_products()
    if products:
        for product in products:
            caption = (f"Заполненный товар: \n"
                       f"Название - {product['name_product']}\n"
                       f"Категория - {product['category']}\n"
                       f"Размер - {product['size']}\n"
                       f"Цена - {product['price']}\n"
                       f"Артикул - {product['product_id']}\n")
            await callback_query.message.answer_photo(
                photo=product['photo'],
                caption=caption
            )
    else:
        await callback_query.message.answer(text='В базе товаров нет!')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands='products')
    dp.register_callback_query_handler(send_all_products, Text(equals='all'))