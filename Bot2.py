import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
from aiogram.types import FSInputFile

logging.basicConfig(level = logging.DEBUG)

api = ''
bot = Bot(token = api)
storage = MemoryStorage()
dp = Dispatcher(storage=MemoryStorage())
router = Router()


class UserState(StatesGroup):
    name = State()
    age = State()
    growth = State()
    weight = State()


    @router.message(Command('start'))
    async def start_massage(message: types.Message, state:FSMContext):
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
            [
             types.KeyboardButton(text = 'Результат'),
             types.KeyboardButton(text = 'Информация'),
             types.KeyboardButton(text = 'Купить')
            ]
        ],
            resize_keyboard= True)
        await message.answer('Добро Пожаловать в калькулятор калорий! Выберите кнопку:', reply_markup=keyboard)
        await state.update_data(start=message.text)

        user_data = await state.get_data()
        await state.set_state(UserState.name)


    @router.message(lambda message: message.text.lower() == 'результат')
    async def main_menu(message:types.Message):
        keyiinline = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Расчитать норму калорий', callback_data='calories')],
                             [InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')],
                             ])

        await message.answer('Выберите опцию:', reply_markup=keyiinline)

    @router.callback_query(lambda call: call.data == 'formulas')
    async def get_formulas(call: types.CallbackQuery):
        formula_get = ("Формула Миффлина-Сан Жеора:\n"
        "BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5 (для мужчин)\n"
        "или\n"
        "BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161 (для женщин)")

        await call.message.answer(formula_get)

    @router.callback_query(lambda call: call.data == 'calories')
    async def set_age(call:types.CallbackQuery, state:FSMContext):
        await call.message.reply('Введите свой возраст:')
        await state.set_state(UserState.age)

    @router.message(age)
    async def set_growth(message:types.Message, state:FSMContext):
        await state.update_data(age = message.text)
        user_data = await state.get_data()
        await message.reply('Введите свой рост:')
        await state.set_state(UserState.growth)

    @router.message(growth)
    async def set_weight(message: types.Message, state:FSMContext):
        await state.update_data(growth = message.text)
        user_data = await state.set_state()
        await message.reply('Введите свой вес:')
        await state.set_state(UserState.weight)

    @router.message(weight)
    async def set_calories(message: types.Message, state:FSMContext):
        await state.update_data(weight = message.text)
        data = await state.get_data()
        age = int(data.get('age'))
        growth = int(data.get('growth'))
        weight = int(data.get('weight'))
        user_data = await state.get_data()
        bmr = 10 * weight + 6.25 * growth - 5 * age + 5

        daily_calories = bmr * 1.2

        await message.answer(f'Ваша норма калорий:{daily_calories:.2f} ккал.')
        await state.clear()

    @router.message(lambda message: message.text.lower() == 'купить')
    async def get_buying_list(message: types.Message):
        photo1 = FSInputFile('photo/1.png')
        await message.answer('Название: Product1 | Описание: описание 1 | Цена: 100')
        await message.answer_photo(photo1)

        photo1 = FSInputFile('photo/2.png')
        await message.answer('Название: Product2 | Описание: описание 2 | Цена: 200')
        await message.answer_photo(photo1)

        photo1 = FSInputFile('photo/3.png')
        await message.answer('Название: Product3 | Описание: описание 3 | Цена: 300')
        await message.answer_photo(photo1)

        photo1 = FSInputFile('photo/4.png')
        await message.answer('Название: Product4 | Описание: описание 4 | Цена: 400')
        await message.answer_photo(photo1)

        key_inline = InlineKeyboardMarkup( inline_keyboard=
                                           [ [InlineKeyboardButton(text='Product1', callback_data='product_buying')],
                                             [InlineKeyboardButton(text='Product2', callback_data='product_buying')],
                                             [InlineKeyboardButton(text='Product3', callback_data='product_buying')],
                                             [InlineKeyboardButton(text='Product4', callback_data='product_buying')] ] )
        await message.answer("Выберите продукт для покупки:", reply_markup=key_inline)




    @router.callback_query(lambda call: call.data == 'product_buying')
    async def send_confirm_message(call: types.CallbackQuery):
        await call.message.answer("Вы успешно приобрели продукт!")



dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


