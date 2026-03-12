from aiogram.dispatcher.filters.state import StatesGroup, State
class Ish(StatesGroup):
    name = State()
    age = State()
    tech = State()
    phone = State()
    adress = State()
    price = State()
    job = State()
    time = State()
    intend = State()

