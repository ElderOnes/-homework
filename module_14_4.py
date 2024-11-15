from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import initiate_db, get_all_products

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация'), KeyboardButton(text='Купить'))

kb_in = InlineKeyboardMarkup()
kb_in.add(
    InlineKeyboardButton(text='Рассчитать норму калорий', callback_data="calories"),
    InlineKeyboardButton(text='Формулы расчёта', callback_data="formulas")
)

kb_buy = InlineKeyboardMarkup()
kb_buy.add(
    InlineKeyboardButton(text='Смеситель', callback_data="product_buying"),
    InlineKeyboardButton(text='Полотенцесушитель', callback_data="product_buying"),
    InlineKeyboardButton(text='Ванна', callback_data="product_buying"),
    InlineKeyboardButton(text='Унитаз', callback_data="product_buying")
)


async def fetch_products():
    return await get_all_products()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=kb_in)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        "Формула Миффлина-Сан Жеора для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()


@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    try:
        users = await fetch_products()
        products = [
            ("file_1.jpg", users[0]),
            ("file_2.jpg", users[1]),
            ("file_3.jpg", users[2]),
            ("file_4.jpg", users[3]),
        ]
        for img_path, user in products:
            with open(img_path, "rb") as img:
                await message.answer_photo(img, f"Название: {user[0]} | Описание: {user[1]} | Цена: {user[2]} руб.")
        await message.answer("Выберите продукт для покупки:", reply_markup=kb_buy)
    except Exception as e:
        await message.answer(f"Ошибка при получении данных: {e}")


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


# Машина состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text="calories")
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer("Введите свой рост:")
        await UserState.growth.set()
    except ValueError:
        await message.answer("Введите числовое значение!")


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    try:
        growth = int(message.text)
        await state.update_data(growth=growth)
        await message.answer("Введите свой вес:")
        await UserState.weight.set()
    except ValueError:
        await message.answer("Введите числовое значение!")


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state):
    try:
        weight = int(message.text)
        data = await state.get_data()
        age, growth = data["age"], data["growth"]
        norma = int(10 * weight + 6.25 * growth - 5 * age + 5)
        await message.answer(f"Ваша норма в сутки: {norma} ккал")
        await state.finish()
    except ValueError:
        await message.answer("Введите числовое значение!")
        await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
