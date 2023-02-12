# importing libraries that we need
import logging

import PIL
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode, InputFile
import aiogram.utils.markdown as md
from io import BytesIO
# importing the bot's token from a separate file
from config import TOKEN_API
import cv2
from PIL import Image
from skimage import io

# configure logging
logging.basicConfig(level=logging.INFO)

# assigning our bot his token and connecting it to a dispatcher
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())


# making a form and setting up fields
class Form(StatesGroup):
    name = State()
    answer_color = State()
    answer_season = State()
    answer_height = State()
    answer_zodiac = State()


# this will output code in Python IDE's terminal that the bot was started
async def on_startup(_):
    print('Bot was successfully started')


# outputs a starting message when /start'ing our bot
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await Form.name.set()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Welcome! Are you ready to learn your life lesson?\nIf so, what is your name?')
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEHraxj51w8MPPGmd7Sn41JftqRHqLAIAACuQMAAkcVaAmDkI2W6g-bmi4E')
    await message.delete()


# inputting name and accepting color
@dp.message_handler(state=Form.name)
async def process_answer_color(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(name=str(message.text))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("❤️", "💙", "💓")
    markup.add("🤍", "💜", "💚")
    markup.add("💛", "🧡")

    await message.answer("What's your favorite color? Choose it from the keyboard below!", reply_markup=markup)


# checking if the color's right
@dp.message_handler(lambda message: message.text not in ["💙", "❤️", "🤍", "💓", "💜", "💚", "💛", "🧡"],
                    state=Form.answer_color)
async def process_answer_color_invalid(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("❤️", "💙", "💓")
    markup.add("🤍", "💜", "💚")
    markup.add("💛", "🧡")
    return await message.reply("I don't know this color. Select a color from the keyboard below.", reply_markup=markup)


# inputting color, accepting season
@dp.message_handler(state=Form.answer_color)
async def process_answer_season(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as data:
        data['answer_color'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Early fall 🍁", "Late fall 🍂")
    markup.add("Early winter ❄️", "Late winter 🌨")
    markup.add("Early spring 🌱", "Late spring 🌸")
    markup.add("Early summer 🌿", "Late summer 🍃")

    await message.reply("What's your favorite time of the year?", reply_markup=markup)


# checking if the season's right
@dp.message_handler(
    lambda message: message.text not in ["Early fall 🍁", "Late fall 🍂", "Early winter ❄️", "Late winter 🌨",
                                         'Early spring 🌱', 'Late spring 🌸', 'Early summer 🌿', 'Late summer 🍃'],
    state=Form.answer_season)
async def process_season_invalid(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Early fall 🍁", "Late fall 🍂")
    markup.add("Early winter ❄️", "Late winter 🌨")
    markup.add("Early spring 🌱", "Late spring 🌸")
    markup.add("Early summer 🌿", "Late summer 🍃")
    return await message.reply("I don't know this season. Select a season from the keyboard below.",
                               reply_markup=markup)


# inputting season, accepting height
@dp.message_handler(state=Form.answer_season)
async def process_answer_height(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as data:
        data['answer_season'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("5' and under (under 152 cm)", "5'1 - 5'4 (152 - 163 cm)")
    markup.add("5'5 - 5'9 (163 - 175 cm)", "5'10 and higher (175 cm and higher)")

    await message.reply("What's your height?", reply_markup=markup)


# checking if the height's right
@dp.message_handler(lambda message: message.text not in ["5' and under (under 152 cm)", "5'1 - 5'4 (152 - 163 cm)",
                                                         "5'5 - 5'9 (163 - 175 cm)",
                                                         "5'10 and higher (175 cm and higher)"],
                    state=Form.answer_height)
async def process_height_invalid(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("5' and under (under 152 cm)", "5'1 - 5'4 (152 - 163 cm)")
    markup.add("5'5 - 5'9 (163 - 175 cm)", "5'10 and higher (175 cm and higher)")
    return await message.reply("I didn't catch your height. Select your height from the keyboard below.",
                               reply_markup=markup)


# inputting height, accepting zodiac
@dp.message_handler(state=Form.answer_height)
async def process_answer_zodiac(message: types.Message, state: FSMContext):
    await Form.next()
    async with state.proxy() as data:
        data['answer_height'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Gemini ♊️ or Cancer ♋️", "Aquarius ♒️ or Pisces ♓️")
    markup.add("Sagittarius ♐️ or Capricorn ♑️", "Aries ♈️ or Taurus ♉️")
    markup.add("Leo ♌️ or Virgo ♍️", "Libra ♎️ or Scorpio ♏️")

    await message.reply("What's your zodiac sign?", reply_markup=markup)


# checking if the zodiac's right
@dp.message_handler(lambda message: message.text not in ["Gemini ♊️ or Cancer ♋️", "Aquarius ♒️ or Pisces ♓️",
                                                         "Sagittarius ♐️ or Capricorn ♑️", "Aries ♈️ or Taurus ♉️",
                                                         "Leo ♌️ or Virgo ♍️", "Libra ♎️ or Scorpio ♏️"],
                    state=Form.answer_zodiac)
async def process_height_invalid(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Gemini ♊️ or Cancer ♋️", "Aquarius ♒️ or Pisces ♓️")
    markup.add("Sagittarius ♐️ or Capricorn ♑️", "Aries ♈️ or Taurus ♉️")
    markup.add("Leo ♌️ or Virgo ♍️", "Libra ♎️ or Scorpio ♏️")
    return await message.reply("I don't know this zodiac sign. Select your sign from the keyboard below.",
                               reply_markup=markup)


# inputting zodiac, picture output
@dp.message_handler(state=Form.answer_zodiac)
async def process_output(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer_zodiac'] = message.text
        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Thank you, ', md.bold(data['name'])),
                md.text('Here is your life lesson:'),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )
        code_from_tg_color = data['answer_color']
        code_from_tg_season = data['answer_season']
        code_from_tg_zodiac = data['answer_zodiac']
        code_from_tg_height = data['answer_height']

        images_all = [f'data/height/{str(code_from_tg_height)}.jpeg',
                      f'data/zodiac/{str(code_from_tg_zodiac)}.jpeg',
                      f'data/season/{str(code_from_tg_season)}.jpeg',
                      f'data/color/{str(code_from_tg_color)}.jpeg']

        # collage maker func
        images_all = [io.imread(img) for img in images_all]
        images_all = [cv2.resize(image, (1920, 1080)) for image in images_all]

        h1 = cv2.hconcat(images_all[:2])
        h2 = cv2.hconcat(images_all[2:])
        concat_images = cv2.vconcat([h1, h2])
        image = Image.fromarray(concat_images)
        # Image path
        image = image.convert("RGB")

        # saves collage to memory instead of a file
        bio = BytesIO()
        image.save(bio, 'JPEG')
        bio.seek(0)
        screenshot = InputFile(bio, "image.jpeg")
        await bot.send_photo(chat_id=message.chat.id, photo=screenshot)

    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Thanks for taking this journey with us!\n'),
            md.text(md.bold('Author of the idea:'), 'SoftGhibliPosts - https://twitter.com/softghibliposts'),
            md.text(md.bold('Original art by:'), 'Studio Ghibli - https://www.ghibli.jp'),
            md.text(md.bold('Bot made by:'), 'Bioinformatics Institute - https://bioinf.me/en\n'),
            md.text('See you soon!'),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEHro9j54clkJAQc6xAu2zkqgsjnUDz7AACogMAAkcVaAnjGJ9ATbovVi4E')


# run long polling
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
