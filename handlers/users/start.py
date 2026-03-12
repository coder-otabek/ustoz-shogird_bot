from aiogram import types
from keyboards.default.start_button import start_button
from loader import dp

@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    text=f"""Assalom alaykum {message.from_user.first_name}
UstozShogird kanalining rasmiy botiga xush kelibsiz!

/help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling!"""
    await message.answer(text,reply_markup=start_button)
