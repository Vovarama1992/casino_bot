from fastapi import FastAPI, HTTPException, Response
from contextlib import asynccontextmanager
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, FSInputFile
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.command import Command
import aiohttp
import aiofiles
import json

# Установим уровень логирования для диагностики
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bot = Bot(token="7326667914:AAGaGAIQKH_-tzGQMnWFis2ZFIddWvXVvfU", default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
app = FastAPI()

ids = []

start_img = FSInputFile(path="start.jpg")

@app.get("/photo/{uid}")
async def get_photo(uid: int):
    logger.info(f"Запрашивается фото для пользователя: {uid}")
    try:
        photos = await bot.get_user_profile_photos(uid)
        if photos.photos:
            url = f"https://api.telegram.org/file/bot{bot.token}/{(await bot.get_file(photos.photos[0][0].file_id)).file_path}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return Response(content=(await resp.read()), status_code=resp.status)
        else:
            raise HTTPException(status_code=404, detail="Фото не найдено")
    except BaseException as e:
        logger.error(f"Ошибка при запросе фото: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера")

kb = [
    [
        InlineKeyboardButton(text='Play', web_app=WebAppInfo(url=f'https://lotos.na4u.ru/'))
    ]
]

async def process_message(message: Message):
    uid = message.from_user.id
    if uid not in ids:
        ids.append(uid)
        async with aiofiles.open("udata.txt", mode="w") as file:
            await file.write(json.dumps(ids))
    logger.info(f"Сообщение от пользователя {uid}: {message.text}")

@dp.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"Команда /start от пользователя {message.from_user.id}")
    await process_message(message)
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer_photo(start_img, caption='Добро пожаловать, в первое лицензированное казино Telegram в мире, представленное lotos.na4u.ru! 💥 Готовы начать? Просто нажмите "Играть сейчас!" и погрузитесь в опыт Lotos - полностью анонимное казино. 🤑', reply_markup=markup)

@dp.message()
async def other(message: Message):
    logger.info(f"Получено сообщение от {message.from_user.username}: {message.text}")
    await process_message(message)
    if message.from_user.username in ["beusefu11"]:
        for _id in ids:
            try:
                await bot.send_message(chat_id=_id, text=message.html_text, parse_mode="HTML")
            except BaseException as e:
                logger.error(f"Ошибка отправки сообщения: {e}")
                pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Логирование старта приложения
    logger.info("Запуск бота...")
    el = asyncio.get_running_loop()
    el.create_task(dp.start_polling(bot))
    yield  # Время выполнения приложения
    logger.info("Остановка бота...")

# Инициализация приложения FastAPI с управлением жизненным циклом
app = FastAPI(lifespan=lifespan)

# Для запуска через FastAPI - uvicorn

