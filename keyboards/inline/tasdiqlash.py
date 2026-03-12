from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="ha"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="yo'q")
        ]
    ]
)