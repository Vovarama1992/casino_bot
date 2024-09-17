import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, BotCommand, User, FSInputFile
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.command import Command
from fastapi import FastAPI, Header, HTTPException, Response
from typing import Annotated
import aiohttp
import aiofiles
import json



logging.basicConfig(level=logging.INFO)
bot = Bot(token="7494241350:AAHbMYhwHx4RsxdhWDN57O6dBcxOx-cKv80", default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
app = FastAPI()

ids = []

start_img = FSInputFile(path="start.jpg")

@app.get("/photo/{uid}")
async def get_photo(uid: int):
    try:
        photos = await bot.get_user_profile_photos(uid)
        if photos.photos:
            url = f"https://api.telegram.org/file/bot{bot.token}/{(await bot.get_file(photos.photos[0][0].file_id)).file_path}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return Response(content=(await resp.read()), status_code=resp.status)
        else:
            raise HTTPException(status_code=404, detail="Photo not found")
    except BaseException as e:
        print(e)
        raise HTTPException(status_code=404, detail="Photo not found")


kb = [
        [   
            InlineKeyboardButton(text='Play', web_app=WebAppInfo(url=f'https://lotos.na4u.ru/'))
            ]
        ]

async def process_message(message: Message):
    uid=message.from_user.id
    if uid not in ids:
        ids.append(uid)
        async with aiofiles.open("udata.txt", mode="w") as file:
            await file.write(json.dumps(ids))

    

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await process_message(message)
    markup = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer_photo(start_img, caption='Добро пожаловать, в первое лицензированное казино Telegram в мире, представленное Lotos-casino.com! 💥 Готовы начать? Просто нажмите "Играть сейчас!" и погрузитесь в опыт Lotos - полностью анонимное казино. 🤑', reply_markup=markup)

@dp.message()
async def other(message: Message):
    await process_message(message)
    if message.from_user.username in ["beusefu11"]:
        for _id in ids:
            try:
                await bot.send_message(chat_id=_id, text=message.html_text, parse_mode="HTML")
            except BaseException as e:
                print(e)
                pass


@dp.startup()
async def on_startup():
    try:
        async with aiofiles.open("udata.txt", mode="r") as file:
            ids.extend(json.loads(await file.read()))
    except FileNotFoundError:
        pass

@dp.shutdown()
async def on_shutdown():
    exit(0)

@app.on_event("startup")
def on_app_startup():
    print(el:=asyncio.get_running_loop())
    el.create_task(dp.start_polling(bot))
