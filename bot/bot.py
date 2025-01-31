import json
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from bot.utils import is_valid_imei, send_api_check_imei_request
from config import BOT_API_TOKEN, TELEGRAM_BOT_TOKEN

from .models import TgUser

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    print(f'Приветствую нового пользователя с ID {message.from_user.id}! ')
    await message.answer("""Привет! Я бот для проверки устройств по IMEI\nВведите  для проверки IMEI""")
    


@dp.message()
async def handle_imei(message: types.Message):
    
    if not await TgUser.check_user_in_whitelist(message.from_user.id):
        await message.answer("Вы не можете выполнить проверку IMEI, так как вас нет в белом списке пользователей. Обратитесь к администратору")
        return

    imei = message.text

    if not is_valid_imei(imei):
        await message.answer("Вы ввели неправильный IMEI")
        return

    info = await send_api_check_imei_request(imei, BOT_API_TOKEN)
    print(info)
    details = info["info"]["detail"]
    json_response = json.dumps(details, ensure_ascii=False, indent=4)
    await message.answer(f"Вот информация по запрошенному IMEI:\n{json_response}")
    

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True) 
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print("Exception: ", e)
        
if __name__ == "__main__":
    asyncio.run(start_bot())