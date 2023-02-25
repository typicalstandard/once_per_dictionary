import logging
import lingua
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from googletrans import Translator,LANGUAGES
from keyboard import get_start_ikb
from langdetect import detect

import db
import gg

translator = Translator()

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5853218890:AAGCcrwF6XAWLvMFlx-PjUtd58BnEiClbzg'


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    text = State()  # Will be represented in storage as 'Form:name'
    translation = State()
    language = State()  # Will be represented in storage as 'Form:age'
    word = State()


async  def on_startup(_):
    await  db.get_all_products()
    print('подключение к БД')


@dp.message_handler(commands=['db'])
async def cmd_start(message: types.Message):
    await message.answer('Словарь',reply_markup=get_start_ikb())


@dp.callback_query_handler(text='get_all_product')
async  def  cb_get_all_product(callback: types.CallbackQuery):
     products = await db.get_all_products()
     if not products:
         await callback.message.answer('НЕТ')
     else:
            await callback.message.answer(products)



@dp.callback_query_handler(text='add_new_product')
async  def cb_add_new_product(callback:types.CallbackQuery)-> None:
    await callback.message.answer('Добавляй')

    await Form.word.set()

@dp.message_handler(state=Form.word)
async def handle_name(message:types.Message,state: FSMContext) -> None:
    async with state.proxy() as data:
        data['word'] = message.text
        if detect(data['word']) != 'ru':
            translation  = translator.translate(data['word'], scr=detect(data['word']), dest='ru')
    await db.create_new_product(data['word'],translation.text)

    await state.finish()


@dp.message_handler(commands=['trans'])
async def user_register(message: types.Message):
    await message.answer("Введите текст для перевода")
    await Form.text.set()


@dp.message_handler(state=Form.text)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    if detect(data['text']) != 'ru':
        await message.answer(translator.translate(data['text'],scr = detect(data['text']) ,dest= 'ru'))
    else:
        await message.answer("Отлично! Теперь выбери язык")
        await Form.language.set()

@dp.message_handler(state=Form.language)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(lanuage=message.text)
    async with state.proxy() as data:
        data['language'] = message.text
    await message.answer(translator.translate(data['text'],scr = 'ru' ,dest= data['language']).text)

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)