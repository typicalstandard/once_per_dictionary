from aiogram.types import  InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


product_cb= CallbackData('name')

def get_start_ikb( )-> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton('просмотр моего члена',callback_data = 'get_all_product')],
                                                [InlineKeyboardButton('+',callback_data = 'add_new_product')]])

    return ikb

def get_cancel_kb()-> ReplyKeyboardMarkup:
    kb  =ReplyKeyboardMarkup(keyboard=[
        [InlineKeyboardButton('/cancel')]
    ])

