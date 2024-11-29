import asyncio
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import sqlite3
from config import TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db(): # Создание базы данных и таблицы
	conn = sqlite3.connect('school_data.db')
	cur = conn.cursor()
	cur.execute('''
	CREATE TABLE IF NOT EXISTS school (  
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	age INTEGER NOT NULL,
	grade TEXT NOT NULL)
	''')
	conn.commit()
	conn.close()

init_db()

# Ожидание ответа Form.name
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Ваше имя")
    await state.set_state(Form.name)

# Ожидание ответа Form.age
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # сохранение имени пользователя в контексте состояния
    await message.answer("Ваш возраст")
    await state.set_state(Form.age)

# Ожидание ответа Form.age
@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком Вы классе")
    await state.set_state(Form.grade)

# Cохранениt ответа о классе
@dp.message(Form.grade)
async def grade(message: Message, state:FSMContext):
    await state.update_data(grade=message.text)
    school_data = await state.get_data() # сохранение введенных данных

    conn = sqlite3.connect('school_data.db')  # введение данных в БД
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO school (name, age, grade) VALUES (?, ?, ?)''', (school_data['name'], school_data['age'], school_data['grade']))
    conn.commit()
    conn.close()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())