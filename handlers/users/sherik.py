from aiogram import types
from keyboards.inline.tasdiqlash import button
from keyboards.default.contact import contact
from states.sherik import Sherik
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import GROUP_ID
from keyboards.default.start_button import start_button

@dp.message_handler(text="Sherik kerak")
async def sherik_start(message: types.Message):
    await message.answer(text="""<b>Sherik topish uchun ariza berish</b>

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""", parse_mode="HTML")

    await message.answer(text="""<b>Ism, familiyangizni kiriting?</b>""", parse_mode="HTML")
    await Sherik.name.set()


@dp.message_handler(state=Sherik.name)
async def sherik_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})

    text = """<b>📚 Texnologiya:</b>

Talab qilinadigan texnologiyalarni kiriting?
Texnologiya nomlarini vergul bilan ajrating. Masalan, 

Java, C++, C#"""
    await message.answer(text=text, parse_mode="HTML")
    await Sherik.tech.set()


@dp.message_handler(state=Sherik.tech)
async def sherik_tech(message: types.Message, state: FSMContext):
    tech = message.text
    await state.update_data({"tech": tech})

    await message.answer("""<b>📞 Aloqa:</b> 

Bog`lanish uchun raqamingizni jo'nating""",
                         parse_mode="HTML",
                         reply_markup=contact)

    await Sherik.phone.set()


# ❌ OLDINGI XATO: state va message argumentlari noto'g'ri edi
# ✅ TO‘G‘RILANGAN:
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Sherik.phone)
async def sherik_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data({"phone": phone})

    await message.answer("""<b>🌐 Hudud:</b> 

Qaysi hududdansiz?
Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.""", parse_mode="HTML")

    await Sherik.adress.set()


@dp.message_handler(state=Sherik.adress)
async def sherik_adress(message: types.Message, state: FSMContext):
    adress = message.text
    await state.update_data({"adress": adress})

    await message.answer("""<b>💰 Narxi:</b>

Tolov qilasizmi yoki Tekinmi?
Kerak bo`lsa, Summani kiriting?""", parse_mode="HTML")

    await Sherik.price.set()


@dp.message_handler(state=Sherik.price)
async def sherik_price(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data({"price": price})

    await message.answer("""<b>👨🏻‍💻 Kasbi:</b> 

Ishlaysizmi yoki o`qiysizmi?
Masalan, Talaba""", parse_mode="HTML")

    await Sherik.job.set()


@dp.message_handler(state=Sherik.job)
async def sherik_job(message: types.Message, state: FSMContext):
    job = message.text
    await state.update_data({"job": job})

    await message.answer("""<b>🕰 Murojaat qilish vaqti: </b>

Qaysi vaqtda murojaat qilish mumkin?
Masalan, 9:00 - 18:00""", parse_mode="HTML")

    await Sherik.time.set()


@dp.message_handler(state=Sherik.time)
async def sherik_time(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data({"time": time})

    await message.answer("""<b>🔎 Maqsad: </b>

Maqsadingizni qisqacha yozib bering.""", parse_mode="HTML")

    await Sherik.intend.set()


@dp.message_handler(state=Sherik.intend)
async def sherik_finish(message: types.Message, state: FSMContext):
    intend = message.text
    await state.update_data({"intend": intend})

    malumotlar = await state.get_data()

    text = "<b>Sherik:</b>\n\n\n"
    text += f"🏅 Sherik: <b>{malumotlar['name']}</b>\n"
    text += f"📚 Texnologiya: <b>{malumotlar['tech']}</b>\n"
    text += f"🇺🇿 Telegram: @{message.from_user.username}\n"
    text += f"📞 Aloqa: <b>{malumotlar['phone']}</b>\n"
    text += f"🌐 Hudud: <b>{malumotlar['adress']}</b>\n"
    text += f"💰 Narxi: <b>{malumotlar['price']}</b>\n"
    text += f"👨🏻‍💻 Kasbi: <b>{malumotlar['job']}</b>\n"
    text += f"🕰 Murojaat qilish vaqti: <b>{malumotlar['time']}</b>\n"
    text += f"🔎 Maqsad: <b>{malumotlar['intend']}</b>\n\n"
    text += "#sherik"

    await state.update_data({"summary": text})     # CALLBACK uchun saqlab qo'yamiz

    await message.answer(text, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=button)


# ❗ TASDIQLASH TUGMASI HANDLERI TO‘G‘RI STATE
@dp.callback_query_handler(state=Sherik.intend)
async def tasdiqlash_handler(call: types.CallbackQuery, state: FSMContext):

    if call.data == "yo'q":
        await call.message.answer("Qabul qilinmadi",reply_markup=start_button)
        await call.message.answer("/start so`zini bosing. E'lon berish qaytadan boshlanadi️")
        try:
            await state.finish()
        except KeyError:
            # foydalanuvchi allaqachon state dan tozalangan bo‘lsa, xatoni e’tiborsiz qoldiramiz
            pass

        except Exception as e:
            await call.message.answer(f"Xatolik yuz berdi: {e}")
    else:
        malumotlar = await state.get_data()
        text = malumotlar["summary"]

        await call.message.answer("""<b>📪 So`rovingiz tekshirish uchun adminga jo`natildi!</b>

E'lon 24-48 soat ichida kanalda chiqariladi.""", parse_mode="HTML",reply_markup=start_button)

        await call.message.answer("/start so`zini bosing. E'lon berish qaytadan boshlanadi️")

        await bot.send_message(chat_id=GROUP_ID, text=text, parse_mode="HTML")

        try:
            await state.finish()
        except KeyError:
            # foydalanuvchi allaqachon state dan tozalangan bo‘lsa, xatoni e’tiborsiz qoldiramiz
            pass

        except Exception as e:
            await call.message.answer(f"Xatolik yuz berdi: {e}")
