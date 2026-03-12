from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import GROUP_ID
from keyboards.inline.tasdiqlash import button
from keyboards.default.contact import contact
from keyboards.default.start_button import start_button
from states.shogird import Shogird


# 1️⃣ Ariza boshlash
@dp.message_handler(text="Shogird kerak")
async def shogird_start(message: types.Message):
    await message.answer(
        "<b>Shogird topish uchun ariza berish</b>\n\n"
        "Hozir sizga birnecha savollar beriladi. "
        "Har biriga javob bering. "
        "Oxirida agar hammasi to‘g‘ri bo‘lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.",
        parse_mode="HTML"
    )
    await message.answer("<b>Ism, familiyangizni kiriting?:</b>", parse_mode="HTML")
    await Shogird.name.set()


# 2️⃣ Ustoz nomi
@dp.message_handler(state=Shogird.name)
async def shogird_name(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer("""<b>🌐 Yosh:"
                         "Yoshingizni kiriting?
Masalan, 19</b>""", parse_mode="HTML")
    await Shogird.age.set()


# 3️⃣ Yosh
@dp.message_handler(state=Shogird.age)
async def shogird_age(message: types.Message, state: FSMContext):
    await state.update_data({"age": message.text})
    await message.answer(
        """<b>📚 Texnologiya:

Talab qilinadigan texnologiyalarni kiriting?
Texnologiya nomlarini vergul bilan ajrating. Masalan, 

Java, C++, C#""",
        parse_mode="HTML"
    )
    await Shogird.tech.set()


# 4️⃣ Texnologiya
@dp.message_handler(state=Shogird.tech)
async def shogird_tech(message: types.Message, state: FSMContext):
    await state.update_data({"tech": message.text})
    await message.answer(
        "<b>📞 Aloqa:</b>\nBog‘lanish uchun raqamingizni jo‘nating",
        parse_mode="HTML",
        reply_markup=contact
    )
    await Shogird.phone.set()


# 5️⃣ Telefon
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Shogird.phone)
async def shogird_phone(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer("<b>🌐 Hudud:</b>\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki\nRespublikani kiriting.", parse_mode="HTML")
    await Shogird.adress.set()


# 6️⃣ Hudud
@dp.message_handler(state=Shogird.adress)
async def shogird_adress(message: types.Message, state: FSMContext):
    await state.update_data({"adress": message.text})
    await message.answer("<b>💰 Narxi:</b>\nTolov qilasizmi yoki tekin?\nKerak bo`lsa, Summani kiriting?", parse_mode="HTML")
    await Shogird.price.set()


# 7️⃣ Narxi
@dp.message_handler(state=Shogird.price)
async def shogird_price(message: types.Message, state: FSMContext):
    await state.update_data({"price": message.text})
    await message.answer("<b>👨🏻‍💻 Kasbi:</b>\n\nIshlaysizmi yoki o`qiysizmi?\nMasalan, Talaba", parse_mode="HTML")
    await Shogird.job.set()


# 8️⃣ Kasbi
@dp.message_handler(state=Shogird.job)
async def shogird_job(message: types.Message, state: FSMContext):
    await state.update_data({"job": message.text})
    await message.answer("<b>🕰 Murojaat qilish vaqti:</b>\n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00-18:00", parse_mode="HTML")
    await Shogird.time.set()


# 9️⃣ Murojaat vaqti
@dp.message_handler(state=Shogird.time)
async def shogird_time(message: types.Message, state: FSMContext):
    await state.update_data({"time": message.text})
    await message.answer("<b>🔎 Maqsad:</b>\nQisqacha maqsadingizni yozing", parse_mode="HTML")
    await Shogird.intend.set()


# 10️⃣ Maqsad va yakun
@dp.message_handler(state=Shogird.intend)
async def shogird_finish(message: types.Message, state: FSMContext):
    await state.update_data({"intend": message.text})
    malumotlar = await state.get_data()

    summary = (
        f"shogird kerak:\n\n"
        f"🎓 Ustoz: {malumotlar['name']}\n"
        f"🌐 Yosh: {malumotlar['age']}\n"
        f"📚 Texnologiya: {malumotlar['tech']}\n"
        f"🇺🇿 Telegram: @{message.from_user.username}\n"
        f"📞 Aloqa: {malumotlar['phone']}\n"
        f"🌐 Hudud: {malumotlar['adress']}\n"
        f"💰 Narxi: {malumotlar['price']}\n"
        f"👨🏻‍💻 Kasbi: {malumotlar['job']}\n"
        f"🕰 Murojaat qilish vaqti: {malumotlar['time']}\n"
        f"🔎 Maqsad: {malumotlar['intend']}\n\n"
        f"#shogird"
    )

    await state.update_data({"summary": summary})
    await message.answer(summary, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=button)


# 11️⃣ Tasdiqlash tugmasi handler
@dp.callback_query_handler(state=Shogird.intend)
async def shogird_confirm(call: types.CallbackQuery, state: FSMContext):
    try:
        malumotlar = await state.get_data()
        summary = malumotlar.get("summary", "Ma'lumot topilmadi")

        if call.data == "yo'q":
            await call.message.answer("Qabul qilinmadi", reply_markup=start_button)
            await call.message.answer("/start so'zini bosing. Ariza qaytadan boshlanadi")
        else:
            await call.message.answer(
                "<b>📪 So‘rovingiz tekshirish uchun adminga jo‘natildi!</b>\n\n"
                "E‘lon 24-48 soat ichida kanalda chiqariladi.",
                parse_mode="HTML",
                reply_markup=start_button
            )
            await bot.send_message(chat_id=GROUP_ID, text=summary, parse_mode="HTML")

    except Exception as e:
        await call.message.answer(f"Xatolik yuz berdi: {e}")

    finally:
        try:
            await state.finish()
        except KeyError:
            pass
