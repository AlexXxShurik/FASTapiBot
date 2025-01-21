import sys
import os
import asyncio
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from app.db.crud import get_product
from app.db.session import AsyncSessionLocal

load_dotenv()
API_TOKEN = os.getenv("BOT_API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class GetProductDataCallback(CallbackData, prefix="get_product"):
    action: str

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    button = InlineKeyboardButton(
        text="Получить данные по товару",
        callback_data=GetProductDataCallback(action="add").pack()
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])

    await bot.send_message(chat_id=message.chat.id, text="Привет! Нажмите кнопку ниже, чтобы продолжить.",
                           reply_markup=keyboard)

@dp.callback_query(GetProductDataCallback.filter())
async def handle_product_request(callback_query: types.CallbackQuery, callback_data: GetProductDataCallback):
    if callback_data.action == "add":
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Пожалуйста, отправьте артикул товара.")

@dp.message()
async def handle_product_data(message: types.Message):
    artikul = message.text.strip()
    if artikul.isdigit():
        async with AsyncSessionLocal() as db:
            product = await get_product(db, artikul)
            if product:
                await message.reply(
                    f"Данные продукта: {product.name} \n" 
                    f"Цена: {product.price} рублей\n" 
                    f"Рейтинг: {product.rating} \n"
                    f"Осталось на складе: {product.total_quantity} \n"
                )
            else:
                await message.reply("Продукт не найден.")
    else:
        await message.reply("Артикул должен быть числовым. Пожалуйста, отправьте корректный артикул.")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())