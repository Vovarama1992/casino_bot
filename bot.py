import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, BotCommand
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7326667914:AAGaGAIQKH_-tzGQMnWFis2ZFIddWvXVvfU")
dp = Dispatcher()

def getInlineKeyboard(referral_id):
    # Формируем правильную ссылку, используя реферальный ID
    link = f'https://lotos.na4u.ru/?user_referral_id={referral_id}'
    return [
        [
            InlineKeyboardButton(
                text='Play',
                web_app=WebAppInfo(url=link)
            )
        ]
    ]

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Извлекаем параметр реферера из команды start
    param = message.text.replace('/start ', '')  # Пример: 'ur-48b0a504-c408-40c7-8db5-9fe18067b501'
    referral_id = param[3:]  # Убираем 'ur-' и оставляем только ID реферера

    # Создаем клавиатуру с кнопкой и ссылкой, передавая реферальный ID
    inlineKeyboard = getInlineKeyboard(referral_id)
    markup = InlineKeyboardMarkup(inline_keyboard=inlineKeyboard)

    # Отправляем сообщение с кнопкой
    await message.answer('Добро пожаловать, в первое лицензированное казино Telegram в мире, представленное lotos.na4u.ru! 💥 Готовы начать? Просто нажмите "Играть сейчас!" и погрузитесь в опыт Lotos - полностью анонимное казино. 🤑', reply_markup=markup)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


