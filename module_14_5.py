from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import initiate_db, add_user, is_included

api = "API"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

initiate_db()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton(text='Рассчитать'))
kb.add(KeyboardButton(text='Информация'))
kb.add(KeyboardButton(text='Купить'))
kb.add(KeyboardButton(text='Регистрация'))

kb_buy = InlineKeyboardMarkup(row_width=2)
kb_buy.add(
    InlineKeyboardButton(text='Смеситель', callback_data="buy_sm"),
    InlineKeyboardButton(text='Полотенцесушитель', callback_data="buy_ps"),
    InlineKeyboardButton(text='Ванна', callback_data="buy_vn"),
    InlineKeyboardButton(text='Унитаз', callback_data="buy_un")
)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Регистрация")
async def sing_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text.strip()

    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text.strip()
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text.strip())
        data = await state.get_data()
        add_user(data["username"], data["email"], age)
        await message.answer(f"Пользователь {data['username']} успешно зарегистрирован!")
        await state.finish()
    except ValueError:
        await message.answer("Возраст должен быть числом. Попробуйте ещё раз:")


@dp.message_handler(text="Купить")
async def show_products(message: types.Message):
    await message.answer("Выберите продукт для покупки:", reply_markup=kb_buy)


@dp.callback_query_handler(lambda call: call.data.startswith("buy_"))
async def send_product_info(call: types.CallbackQuery):
    products = {
        "buy_sm": {"name": "Смеситель", "description": "Хромированный смеситель", "price": 2500, "image": "file_1.jpg"},
        "buy_ps": {"name": "Полотенцесушитель", "description": "Электрический полотенцесушитель", "price": 3200,
                   "image": "file_2.jpg"},
        "buy_vn": {"name": "Ванна", "description": "Акриловая ванна", "price": 8000, "image": "file_3.jpg"},
        "buy_un": {"name": "Унитаз", "description": "Подвесной унитаз", "price": 4200, "image": "file_4.jpg"}
    }

    product = products[call.data]
    with open(product["image"], "rb") as img:
        await bot.send_photo(call.message.chat.id, img, caption=f"**Название:** {product['name']}\n"
                                                                f"**Описание:** {product['description']}\n"
                                                                f"**Цена:** {product['price']} руб.",
                             parse_mode="Markdown")
    await call.answer("Спасибо за выбор!")


@dp.message_handler(text="Информация")
async def info(message: types.Message):
    await message.answer("Привет, я бот, помогающий твоему здоровью!")


@dp.message_handler(text="Рассчитать")
async def calculate(message: types.Message):
    await message.answer("Эта функция ещё не реализована.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
