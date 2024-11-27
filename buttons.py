from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



size_list = InlineKeyboardMarkup(row_width=2)
size_list.add(
    InlineKeyboardButton(text='L', callback_data='L'),
    InlineKeyboardButton(text='XL', callback_data='XL'),
    InlineKeyboardButton(text='XXL', callback_data='XXL')
)

confirm_list = InlineKeyboardMarkup(row_width=2)
confirm_list.add(
    InlineKeyboardButton(text='Да', callback_data='Да'),
    InlineKeyboardButton(text='Нет', callback_data='Нет'),
)



a = True
cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=a)
cancel_button = KeyboardButton('Отмена')
cancel.add(cancel_button)