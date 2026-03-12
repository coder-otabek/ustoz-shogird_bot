from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import GROUP_ID
from keyboards.inline.tasdiqlash import button
from keyboards.default.contact import contact
from keyboards.default.start_button import start_button
from states.ustoz import Shogird


# 1️⃣ Ariza boshlash
@dp.message_handler(text="Ustoz kerak")
async def shogird_start(message: types.Message):
    await message.answer(
        "<b>Ustoz topish uchun ariza berish</b>\n\n"
        "Hozir sizga birnecha savollar beriladi. "
        "Har biriga javob bering. "
        "Oxirida agar hammasi to‘g‘ri bo‘lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.",
        parse_mode="HTML"
    )
    await message.answer("<b>Ism, familiyangizni kiriting:</b>", parse_mode="HTML")
    await Shogird.name.set()


# 2️⃣ Ism
@dp.message_handler(state=Shogird.name)
async def shogird_name(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer("<b>🕑 Yoshingizni kiriting:</b>", parse_mode="HTML")
    await Shogird.age.set()


# 3️⃣ Yosh
@dp.message_handler(state=Shogird.age)
async def shogird_age(message: types.Message, state: FSMContext):
    await state.update_data({"age": message.text})
    await message.answer(
        "<b>📚 Texnologiya:</b>\n\nQaysi texnologiyalarda ishlay olasiz yoki o‘rganmoqchisiz? "
        "Texnologiya nomlarini vergul bilan ajrating.",
        parse_mode="HTML"
    )
    await Shogird.tech.set()


# 4️⃣ Texnologiya
@dp.message_handler(state=Shogird.tech)
async def shogird_tech(message: types.Message, state: FSMContext):
    await state.update_data({"tech": message.text})
    await message.answer(
        "<b>📞 Aloqa:</b>\n\nBog‘lanish uchun raqamingizni jo‘nating",
        parse_mode="HTML",
        reply_markup=contact
    )
    await Shogird.phone.set()


# 5️⃣ Telefon
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Shogird.phone)
async def shogird_phone(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer(
        "<b>🌐 Hudud:</b>\n\nQaysi hududdansiz?",
        parse_mode="HTML"
    )
    await Shogird.adress.set()


# 6️⃣ Hudud
@dp.message_handler(state=Shogird.adress)
async def shogird_adress(message: types.Message, state: FSMContext):
    await state.update_data({"adress": message.text})
    await message.answer("<b>✍️ Mas'ul:</b>\n\nKim murojaat qiladi?", parse_mode="HTML")
    await Shogird.price.set()


# 7️⃣ Mas'ul / Narxi
@dp.message_handler(state=Shogird.price)
async def shogird_price(message: types.Message, state: FSMContext):
    await state.update_data({"price": message.text})
    await message.answer(
        "<b>🕰 Murojaat vaqti:</b>\n\nQaysi vaqtda murojaat qilish mumkin?",
        parse_mode="HTML"
    )
    await Shogird.time.set()


# 8️⃣ Murojaat vaqti
@dp.message_handler(state=Shogird.time)
async def shogird_time(message: types.Message, state: FSMContext):
    await state.update_data({"time": message.text})
    await message.answer(
        "<b>🕰 Ish vaqti:</b>\n\nIsh vaqti qanday bo‘ladi?",
        parse_mode="HTML"
    )
    await Shogird.job.set()


# 9️⃣ Ish vaqti
@dp.message_handler(state=Shogird.job)
async def shogird_job(message: types.Message, state: FSMContext):
    await state.update_data({"job": message.text})
    await message.answer("<b>💰 Maosh:</b>\n\nMaosh miqdorini kiriting", parse_mode="HTML")
    await Shogird.intend.set()


# 10️⃣ Maosh
@dp.message_handler(state=Shogird.intend)
async def shogird_intend(message: types.Message, state: FSMContext):
    await state.update_data({"intend": message.text})
    await message.answer("<b>‼️ Qo‘shimcha ma‘lumot:</b>\n\nQo‘shimcha yozing yoki '-' kiriting", parse_mode="HTML")
    await Shogird.extra.set()


# 11️⃣ Qo‘shimcha va yakun
@dp.message_handler(state=Shogird.extra)
async def shogird_finish(message: types.Message, state: FSMContext):
    await state.update_data({"extra": message.text})
    malumotlar = await state.get_data()

    summary = (
        f"Ustoz kerak:\n\n"
        f"🏅 Ism: {malumotlar['name']}\n"
        f"🕑 Yosh: {malumotlar['age']}\n"
        f"📚 Texnologiya: {malumotlar['tech']}\n"
        f"🇺🇿 Telegram: @{message.from_user.username}\n"
        f"📞 Aloqa: {malumotlar['phone']}\n"
        f"🌐 Hudud: {malumotlar['adress']}\n"
        f"✍️ Mas'ul: {malumotlar['price']}\n"
        f"🕰 Murojaat vaqti: {malumotlar['time']}\n"
        f"🕰 Ish vaqti: {malumotlar['job']}\n"
        f"💰 Maosh: {malumotlar['intend']}\n"
        f"‼️ Qo‘shimcha: {malumotlar['extra']}\n\n"
        f"#shogird"
    )

    await state.update_data({"summary": summary})
    await message.answer(summary, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=button)


# 12️⃣ Tasdiqlash tugmasi handler
@dp.callback_query_handler(state=Shogird.extra)
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
