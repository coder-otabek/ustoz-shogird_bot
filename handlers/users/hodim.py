from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from data.config import GROUP_ID
from keyboards.inline.tasdiqlash import button
from keyboards.default.contact import contact
from keyboards.default.start_button import start_button
from states.hodim import Hodim


@dp.message_handler(text="Hodim kerak")
async def hodim_start(message: types.Message):
    await message.answer(
        text="""<b>Ish joyi topish uchun ariza berish</b>

Hozir sizga birnecha savollar beriladi. 
Har biriga javob bering. 
Oxirida agar hammasi to'g'ri bo'lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.""",
        parse_mode="HTML"
    )
    await message.answer("<b>🏢 Idora nomini kiriting:</b>", parse_mode="HTML")
    await Hodim.name.set()


@dp.message_handler(state=Hodim.name)
async def hodim_name(message: types.Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer("<b>🕑 Yoshingizni kiriting:</b>", parse_mode="HTML")
    await Hodim.age.set()


@dp.message_handler(state=Hodim.age)
async def hodim_age(message: types.Message, state: FSMContext):
    await state.update_data({"age": message.text})
    await message.answer(
        "<b>📚 Texnologiya:</b>\n\nTalab qilinadigan texnologiyalarni kiriting. "
        "Texnologiya nomlarini vergul bilan ajrating. Masalan, Java, C++, C#",
        parse_mode="HTML"
    )
    await Hodim.tech.set()


@dp.message_handler(state=Hodim.tech)
async def hodim_tech(message: types.Message, state: FSMContext):
    await state.update_data({"tech": message.text})
    await message.answer(
        "<b>📞 Aloqa:</b>\n\nBog'lanish uchun raqamingizni jo'nating",
        parse_mode="HTML",
        reply_markup=contact
    )
    await Hodim.phone.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=Hodim.phone)
async def hodim_phone(message: types.Message, state: FSMContext):
    await state.update_data({"phone": message.contact.phone_number})
    await message.answer(
        "<b>🌐 Hudud:</b>\n\nQaysi hududdansiz? Viloyat nomi, Toshkent shahar yoki Respublikani kiriting.",
        parse_mode="HTML"
    )
    await Hodim.adress.set()


@dp.message_handler(state=Hodim.adress)
async def hodim_adress(message: types.Message, state: FSMContext):
    await state.update_data({"adress": message.text})
    await message.answer("<b>✍️ Mas'ul:</b>\n\nKim murojaat qiladi?", parse_mode="HTML")
    await Hodim.price.set()


@dp.message_handler(state=Hodim.price)
async def hodim_price(message: types.Message, state: FSMContext):
    await state.update_data({"price": message.text})
    await message.answer(
        "<b>🕰 Murojaat vaqti:</b>\n\nQaysi vaqtda murojaat qilish mumkin? Masalan, 9:00 - 18:00",
        parse_mode="HTML"
    )
    await Hodim.time.set()


@dp.message_handler(state=Hodim.time)
async def hodim_time(message: types.Message, state: FSMContext):
    await state.update_data({"time": message.text})
    await message.answer(
        "<b>🕰 Ish vaqti:</b>\n\nIsh vaqti qanday bo‘ladi? Masalan, 9:00 - 17:00",
        parse_mode="HTML"
    )
    await Hodim.job.set()


@dp.message_handler(state=Hodim.job)
async def hodim_job(message: types.Message, state: FSMContext):
    await state.update_data({"job": message.text})
    await message.answer("<b>💰 Maosh:</b>\n\nMaosh miqdorini kiriting", parse_mode="HTML")
    await Hodim.intend.set()


@dp.message_handler(state=Hodim.intend)
async def hodim_intend(message: types.Message, state: FSMContext):
    await state.update_data({"intend": message.text})
    await message.answer("<b>‼️ Qo'shimcha ma'lumot:</b>\n\nQo'shimcha yozing yoki '-' kiriting", parse_mode="HTML")
    await Hodim.extra.set()


@dp.message_handler(state=Hodim.extra)
async def hodim_finish(message: types.Message, state: FSMContext):
    await state.update_data({"extra": message.text})
    malumotlar = await state.get_data()

    summary = (
        f"Xodim kerak:\n\n"
        f"🏢 Idora: {malumotlar['name']}\n"
        f"📚 Texnologiya: {malumotlar['tech']}\n"
        f"🇺🇿 Telegram: @{message.from_user.username}\n"
        f"📞 Aloqa: {malumotlar['phone']}\n"
        f"🌐 Hudud: {malumotlar['adress']}\n"
        f"✍️ Mas'ul: {malumotlar['price']}\n"
        f"🕰 Murojaat vaqti: {malumotlar['time']}\n"
        f"🕰 Ish vaqti: {malumotlar['job']}\n"
        f"💰 Maosh: {malumotlar['intend']}\n"
        f"‼️ Qo`shimcha: {malumotlar['extra']}\n\n"
        f"#ishJoyi"
    )

    await state.update_data({"summary": summary})
    await message.answer(summary, parse_mode="HTML")
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=button)


@dp.callback_query_handler(state=Hodim.extra)
async def hodim_confirm(call: types.CallbackQuery, state: FSMContext):
    try:
        malumotlar = await state.get_data()
        summary = malumotlar.get("summary", "Ma'lumot topilmadi")

        if call.data == "yo'q":
            await call.message.answer("Qabul qilinmadi", reply_markup=start_button)
            await call.message.answer("/start so'zini bosing. E'lon berish qaytadan boshlanadi️")
        else:
            await call.message.answer(
                "<b>📪 So`rovingiz tekshirish uchun adminga jo`natildi!</b>\n\n"
                "E'lon 24-48 soat ichida kanalda chiqariladi.",
                parse_mode="HTML",
                reply_markup=start_button
            )
            await call.message.answer("/start so`zini bosing. E'lon berish qaytadan boshlanadi️")
            await bot.send_message(chat_id=GROUP_ID, text=summary, parse_mode="HTML")

    except Exception as e:
        await call.message.answer(f"Xatolik yuz berdi: {e}")

    finally:
        try:
            await state.finish()
        except KeyError:
            pass
