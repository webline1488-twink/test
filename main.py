import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# ТОКЕН бота
TOKEN = "8393976057:AAHB82T-9w05RYw7Oysl4sZ2YrAxwEEfe5A"

# Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! 👋")

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
