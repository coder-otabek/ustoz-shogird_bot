from aiogram import types
from keyboards.inline.tasdiqlash import button
from keyboards.default.contact import contact
from states.ish import Ish
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import GROUP_ID
from keyboards.default.start_button import start_button

@dp.message_handler(text="Ish joyi kerak")
async def ish_start(message: types.Message):
    await message.answer(
        text="""<b>Ish joyi topish uchun ariza berish</b>

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""",
        parse_mode="HTML"
    )
    await message.answer(text="""<b>Ism, familiyangizni kiriting?</b>""", parse_mode="HTML")
    await Ish.name.set()


@dp.message_handler(state=Ish.name)
async def ish_name(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer(text="""<b>🕑 Yoshingizni kiriting:</b>""", parse_mode="HTML")
    await Ish.age.set()


@dp.message_handler(state=Ish.age)
async def ish_age(message: types.Message, state: FSMContext):
    await state.update_data({"age": message.text})
    text = """<b>📚 Texnologiya:</b>

Talab qilinadigan texnologiyalarni kiriting.
Texnologiya nomlarini vergul bilan ajrating. Masalan, 

Java, C++, C#"""
    await message.answer(text=text, parse_mode="HTML")
    await Ish.tech.set()


@dp.message_handler(state=Ish.tech)
async def ish_tech(message: types.Message, state: FSMContext):
    await state.update_data({"tech": message.text})
    await message.answer(
        """<b>📞 Aloqa:</b> 

Bog`lanish uchun raqamingizni jo'nating""",
        parse_mode="HTML",
        reply_markup=contact
    )
    await Ish.phone.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Ish.phone)
async def ish_phone(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer(
        """<b>🌐 Hudud:</b> 

Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.""",
        parse_mode="HTML"
    )
    await Ish.adress.set()


@dp.message_handler(state=Ish.adress)
async def ish_adress(message: types.Message, state: FSMContext):
    await state.update_data({"adress": message.text})
    await message.answer(
        """<b>💰 Narxi:</b>

Tolov qilasizmi yoki tekinmi?
Kerak bo`lsa, summani kiriting.""",
        parse_mode="HTML"
    )
    await Ish.price.set()


@dp.message_handler(state=Ish.price)
async def ish_price(message: types.Message, state: FSMContext):
    await state.update_data({"price": message.text})
    await message.answer(
        """<b>👨🏻‍💻 Kasbi:</b> 

Ishlaysizmi yoki o`qiysizmi?
Masalan, Talaba""",
        parse_mode="HTML"
    )
    await Ish.job.set()


@dp.message_handler(state=Ish.job)
async def ish_job(message: types.Message, state: FSMContext):
    await state.update_data({"job": message.text})
    await message.answer(
        """<b>🕰 Murojaat qilish vaqti: </b>

Qaysi vaqtda murojaat qilish mumkin?
Masalan, 9:00 - 18:00""",
        parse_mode="HTML"
    )
    await Ish.time.set()


@dp.message_handler(state=Ish.time)
async def ish_time(message: types.Message, state: FSMContext):
    await state.update_data({"time": message.text})
    await message.answer(
        """<b>🔎 Maqsad: </b>

Maqsadingizni qisqacha yozib bering.""",
        parse_mode="HTML"
    )
    await Ish.intend.set()


@dp.message_handler(state=Ish.intend)
async def ish_finish(message: types.Message, state: FSMContext):
    await state.update_data({"intend": message.text})

    malumotlar = await state.get_data()

    text = "<b>Ish joyi kerak:</b>\n\n\n"
    text += f"🏅 Sherik: <b>{malumotlar['name']}</b>\n"
    text += f"🕑 Yosh: {malumotlar['age']}\n"
    text += f"📚 Texnologiya: <b>{malumotlar['tech']}</b>\n"
    text += f"🇺🇿 Telegram: @{message.from_user.username}\n"
    text += f"📞 Aloqa: <b>{malumotlar['phone']}</b>\n"
    text += f"🌐 Hudud: <b>{malumotlar['adress']}</b>\n"
    text += f"💰 Narxi: <b>{malumotlar['price']}</b>\n"
    text += f"👨🏻‍💻 Kasbi: <b>{malumotlar['job']}</b>\n"
    text += f"🕰 Murojaat qilish vaqti: <b>{malumotlar['time']}</b>\n"
    text += f"🔎 Maqsad: <b>{malumotlar['intend']}</b>\n\n"
    text += "#xodim"

    await state.update_data({"summary": text})

    await message.answer(text, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=button)


@dp.callback_query_handler(state=Ish.intend)
async def tasdiqlash_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        malumotlar = await state.get_data()
        text = malumotlar.get("summary", "Ma'lumot topilmadi")

        if call.data == "yo'q":
            await call.message.answer("Qabul qilinmadi",reply_markup=start_button)
            await call.message.answer("/start so`zini bosing. E'lon berish qaytadan boshlanadi️")
        else:
            await call.message.answer(
                """<b>📪 So`rovingiz tekshirish uchun adminga jo`natildi!</b>

E'lon 24-48 soat ichida kanalda chiqariladi.""",
                parse_mode="HTML",reply_markup=start_button
            )
            await call.message.answer("/start so`zini bosing. E'lon berish qaytadan boshlanadi️")
            await bot.send_message(chat_id=GROUP_ID, text=text, parse_mode="HTML")

    except Exception as e:
        await call.message.answer(f"Xatolik yuz berdi: {e}")

    finally:
        try:
            await state.finish()
        except KeyError:
            pass
