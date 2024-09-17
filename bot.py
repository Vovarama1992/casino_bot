import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, BotCommand
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7494241350:AAHbMYhwHx4RsxdhWDN57O6dBcxOx-cKv80")
dp = Dispatcher()

def getInlineKeyboard(param):
    link = "https://lotos-casino.net"
    if(param):
        link += f'?{param}'

    return [
                [
                InlineKeyboardButton(text='Play', web_app=WebAppInfo(url=link))
                ]
            ]

@dp.message(Command("start"))
async def cmd_start(message: Message):
    param = message.text.replace('/start ', '')
    referralTypeCode = param[:3]
    paramKey = ""
    if(referralTypeCode == "ri-"):
        # manager link
        paramKey = "referral_invitation_id"
    elif(referralTypeCode == "ur-"):
        # user referral link
        paramKey = "user_referral_id"
    

    paramValue = param[3:]
    parameterKeyValue = None
    if(len(paramKey)>0 and len(paramValue)>0):
        parameterKeyValue = f'{paramKey}={paramValue}'

    inlineKeyboard = getInlineKeyboard(parameterKeyValue)
    print(inlineKeyboard)
    markup = InlineKeyboardMarkup(
            inline_keyboard=inlineKeyboard)

    await message.answer('Добро пожаловать, в первое лицензированное казино Telegram в мире, представленное Lotos-casino.com! 💥 Готовы начать? Просто нажмите "Играть сейчас!" и погрузитесь в опыт Lotos - полностью анонимное казино. 🤑', reply_markup=markup)
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

