
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel, size_list, confirm_list
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery
from db import db_main
from config import bot, Staff



class fsm_order(StatesGroup):
    product_id = State()
    size = State()
    quantity = State()
    phone_number = State()


async def start_fsm(message: types.Message):

        await message.answer('Введите артикул товара: ')
        await fsm_order.product_id.set()

async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text


    await fsm_order.next()
    await message.answer('Выберите размер:', reply_markup=size_list)


async def process_size_select(callback_query: CallbackQuery, state: FSMContext):
    size = callback_query.data
    async with state.proxy() as data:
        data['size'] = size
    await callback_query.answer()

    await fsm_order.next()
    await callback_query.message.answer('Введите количество')


async def load_product_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await fsm_order.next()
    await message.answer('Отправьте Ваш номер телефона')



async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await message.answer('Верные ли данные?:', reply_markup=confirm_list)





async def process_confirm_order(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback_query.data == 'Да':
            for admin in Staff:
                await bot.send_message(chat_id=admin,
                                       text=f'Заполенный заказ: \n'
                                        f"Артикул товара - {data['product_id']}\n"
                                        f"Размер - {data['size']}\n"
                                        f"Количество - {data['quantity']}\n"
                                        f"Номер телефона - {data['phone_number']}\n")


            await state.finish()
        elif callback_query.data == 'Нет':
            await state.finish()




async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb_remove = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено', reply_markup=kb_remove)


def reg_handler_fsm_order(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_fsm, commands=['order'])
    dp.register_message_handler(load_product_id, state=fsm_order.product_id)
    dp.register_callback_query_handler(process_size_select, state=fsm_order.size)
    dp.register_message_handler(load_product_quantity, state=fsm_order.quantity)
    dp.register_message_handler(load_phone_number, state=fsm_order.phone_number)


    dp.register_callback_query_handler(process_confirm_order, Text(equals='Да'), state=fsm_order.phone_number)
    dp.register_callback_query_handler(process_confirm_order, Text(equals='Нет'), state=fsm_order.phone_number)