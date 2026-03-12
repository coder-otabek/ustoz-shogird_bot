from aiogram.dispatcher.filters.state import State, StatesGroup

class Hodim(StatesGroup):
    name = State()
    age = State()
    tech = State()
    phone = State()
    adress = State()
    price = State()
    time = State()
    job = State()
    intend = State()
    extra = State()
