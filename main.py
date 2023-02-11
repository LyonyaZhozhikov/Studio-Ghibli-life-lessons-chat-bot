# imports automated
from aiogram import Bot, executor, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode, InputFile
import aiogram.utils.markdown as md

# comes from BotFather
API_TOKEN = '6137106078:AAGQJTuwL_cLvp8cXBxbm4ECxJUQtmQ9_B4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# создаём форму и указываем поля
class Form(StatesGroup):
    name = State()
    answer_color = State()
    answer_year = State()
    # задание 1

# Начинаем наш диалог
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await Form.name.set()
    await message.reply("Привет!\nЯ демо бот кружочка по биоинформатике!\nКак тебя зовут?")


# Принимаем имя и делаем цвет
@dp.message_handler(state=Form.name)
async def process_age(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(name=str(message.text))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("blue", "цвет2")
    markup.add("цвет3", "цвет4")

    await message.reply("Укажи color (кнопкой)", reply_markup=markup)


# Проверяем цвет
@dp.message_handler(lambda message: message.text not in ["цвет1", "цвет2", "цвет3", "цвет4"], state=Form.answer_color)
async def process_answer_color_invalid(message: types.Message):
    return await message.reply("Не знаю такой цвет. Укажи цвет кнопкой на клавиатуре")


# Сохраняем цвет, выводим year
@dp.message_handler(state=Form.answer_color)
async def process_answer_color(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as data:
        data['answer_color'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("год1", "год2")
    markup.add("год3", "год4")

    await message.reply("Укажи год (кнопкой)", reply_markup=markup)


# Проверяем year
@dp.message_handler(lambda message: message.text not in ["год1", "год2", "год3", "год4"], state=Form.answer_year)
async def process_year_invalid(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("год1", "год2")
    markup.add("год3", "год4")
    return await message.reply("Не знаю такой year. Укажи цвет кнопкой на клавиатуре", reply_markup=markup)


    # задание 1 - добавление новых функций

    # задание 2 -это поработать над стилистикой/оформлением


# Сохраняем year, выводим pictures
@dp.message_handler(state=Form.answer_year)
async def process_year(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer_year'] = message.text
        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Спасибо за прохождение данного теста человек с именем ', md.bold(data['name'])),
                md.text('Ниже будут результаты теста'),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        code_from_tg_color = data['answer_color']
        code_from_tg_year = data['answer_year']
 # цвет1
        photo_color = InputFile(f'data/c-{str(code_from_tg_color)[-1]}.jpeg')
        photo_year = InputFile(f'data/y-{str(code_from_tg_year)[-1]}.jpeg')

        # задание 3 - найти и имплементировать модуль соединяющий 4 картинку в одну
        # и отправляет пользователю
        # module = 1+2+3+4

        # не сохраняет картинку, но при этом дает её в отправку пользователю

        await bot.send_photo(chat_id=message.chat.id, photo=photo_color)
        await bot.send_photo(chat_id=message.chat.id, photo=photo_year)

    await state.finish()
###

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
