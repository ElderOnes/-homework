from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kl = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формула расчёта', callback_data='formulas')
kl.add(button, button2)

kb = InlineKeyboardMarkup()
buttons = [
    InlineKeyboardButton(text=f'Продукт {i}', callback_data='product_buying')
    for i in range(1, 5)
]
kb.add(*buttons)

kp = ReplyKeyboardMarkup(resize_keyboard=True)
kp.add(
    KeyboardButton(text='Рассчитать'),
    KeyboardButton(text='Информация'),
    KeyboardButton(text='Купить')
)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет, я бот, помогающий твоему здоровью!', reply_markup=kp)


@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Я помогу рассчитать вашу норму калорий, а также предложу товары для здоровья.')


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=kl)


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    for i in range(1, 5):
        try:
            with open(f'files/{i}.jpg', 'rb') as img:
                await message.answer_photo(img, f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}р')
        except FileNotFoundError:
            await message.answer(f'Файл для Product{i} не найден.')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer('Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    try:
        age = int(message.text)
        await state.update_data(age=age)
        await message.answer('Введите свой рост:')
        await UserState.growth.set()
    except ValueError:
        await message.answer('Пожалуйста, введите числовое значение.')


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    try:
        growth = int(message.text)
        await state.update_data(growth=growth)
        await message.answer('Введите свой вес:')
        await UserState.weight.set()
    except ValueError:
        await message.answer('Пожалуйста, введите числовое значение.')


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state):
    try:
        weight = int(message.text)
        await state.update_data(weight=weight)
        data = await state.get_data()
        age = data['age']
        growth = data['growth']
        weight = data['weight']
        calories = 10 * weight + 6.25 * growth - 5 * age + 5
        await message.answer(f"Ваша дневная норма калорий: {calories} ккал")
    except ValueError:
        await message.answer('Пожалуйста, введите числовое значение.')
    finally:
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
