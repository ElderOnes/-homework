from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = '***'
bot = Bot(token=api)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Рассчитать'), KeyboardButton('Информация'))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Привет! Выберите действие:",
        reply_markup=keyboard
    )


@dp.message_handler(text='Рассчитать')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    try:
        age = float(data['age'])
        weight = float(data['weight'])
        growth = float(data['growth'])
    except ValueError:
        await message.answer('Не могу конвертировать введенные значения в числа.')
        await state.finish()
        return

    calories_man = 10 * weight + 6.25 * growth - 5 * age + 5
    calories_wom = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Норма (муж.): {calories_man:.2f} ккал')
    await message.answer(f'Норма (жен.): {calories_wom:.2f} ккал')
    await state.finish()


@dp.message_handler(text='Информация')
async def information(message: types.Message):
    await message.answer(
        "Это бот для расчёта нормы калорий. Нажмите 'Рассчитать', чтобы начать ввод данных."
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
