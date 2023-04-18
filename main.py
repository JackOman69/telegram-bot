import logging
from typing import Mapping, Any
from aiohttp import ClientSession
from random import randint
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from url_backends import URL_BACKENDS, ENDPOINT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
server_url = ""
code = ""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global server_url
    global code
    # try:
    client_args = context.args[0].split("-")
    server_url = URL_BACKENDS[client_args[0]] + ENDPOINT
    code = client_args[1]
    params = {
        "code": code
    }
    async with ClientSession() as session:
        await session.request(url=server_url, params=params,method="POST")
    # except:
    #     client_args = ""
    keyboard = [
        [KeyboardButton("Поделиться номером", request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Я бот который используется для авторизации\nДля того чтобы войти в аккаунт, пожалуйста, нажмите на кнопку ниже, чтобы поделиться своим номером телефона с ботом\nПосле проверки вы сможете войти/зарегистрироваться в приложение", reply_markup=reply_markup)

async def shared_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global server_url
    global code
    if update.message.contact is not None:
        phone_number = update.message.contact.phone_number
        params = {
            "phone": phone_number.replace("+",""),
            "code": code
        }
        async with ClientSession() as session:
            await session.request(url=server_url, params=params,method="POST")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Contact shared: {phone_number}")
        
if __name__ == '__main__':
    
    application = ApplicationBuilder().token('5919785165:AAHPyH-9m6MahcjZvqcajHw4LrhIEcIKQRk').build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.CONTACT, shared_contact))
    application.run_polling()