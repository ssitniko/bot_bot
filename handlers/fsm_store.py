
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel, size_list, confirm_list
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery
from db import db_main
from config import bot, Staff



class fsm_store(StatesGroup):
    name_product = State()
    category = State()
    size = State()
    price = State()
    product_id = State()
    photo = State()


async def start_fsm(message: types.Message):
    if message.from_user.id not in Staff:
        await message.answer('У Вас нет прав вводить товары в базу данных: ')

    else:
        await message.answer('Введите название товара: ')
        await fsm_store.name_product.set()

async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text


    await fsm_store.next()
    await message.answer('Введите категорию товара')


async def load_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await fsm_store.next()
    await message.answer('Выберите размер:', reply_markup=size_list)



async def process_size_select(callback_query: CallbackQuery, state: FSMContext):
    size = callback_query.data
    async with state.proxy() as data:
        data['size'] = size
    await callback_query.answer()

    await fsm_store.next()
    await callback_query.message.answer('Введите стоимость товара')


async def load_product_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await fsm_store.next()
    await message.answer('Введите артикул товара')



async def product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['product_id'] = int(message.text)
            await fsm_store.next()
            await message.answer('Отправьте фото:')
        else:
            await message.answer('Введите артикул только цифрами')
            await fsm_store.product_id.set()


async def load_product_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    # await state.finish()
    await message.answer_photo(photo=data['photo'],
                               caption= f'Название товара - {data["name_product"]}\n'
                                        f'Категория - {data["category"]}\n'
                                        f'Размер - {data["size"]}\n'
                                        f'Цена - {data["price"]}\n'
                                        f'Артикул - {data["product_id"]}\n')



    await message.answer('Верные ли данные?:', reply_markup=confirm_list)



async def submit(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'Да':
        await callback_query.message.answer('Отлично, товар в базе!')

        async with state.proxy() as data:
            await db_main.sql_insert_store(
                name_product=data['name_product'],
                category=data['category'],
                size=data['size'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo']
            )

    elif callback_query.data == 'Нет':
        await callback_query.message.answer('Отменено!')

    else:
        await callback_query.answer('Введите Да или Нет')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb_remove = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено', reply_markup=kb_remove)



def reg_handler_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_fsm, commands=['store'])
    dp.register_message_handler(load_name_product, state=fsm_store.name_product)
    dp.register_message_handler(load_product_category, state=fsm_store.category)
    dp.register_callback_query_handler(process_size_select, state=fsm_store.size)
    dp.register_message_handler(load_product_price, state=fsm_store.price)
    dp.register_message_handler(product_id, state=fsm_store.product_id)
    dp.register_message_handler(load_product_photo, state=fsm_store.photo, content_types=['photo'])

    dp.register_callback_query_handler(submit, Text(equals='Да'), state=fsm_store.photo)
    dp.register_callback_query_handler(submit, Text(equals='Нет'), state=fsm_store.photo)


