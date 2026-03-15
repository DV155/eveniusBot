from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes, 
    CallbackQueryHandler
)
import yfinance as yf
import os
import logging
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("API_TOKEN")
BOT_USERNAME = os.getenv("BOT_HANDLE")
MENU, AWAITING_INPUT = range(2)
lang = None
lookingForStock = False
answer = None

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇬🇧", callback_data="option1")],
        [InlineKeyboardButton("🇩🇪", callback_data="option2")],
        [InlineKeyboardButton("🇷🇺", callback_data="option3")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello! I am Evenius, your bot for sourcing stock prices in real time. Please choose your language:", reply_markup=reply_markup
    )
    return MENU

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    global lang
    global answer

    if query.data == "option1":
        await query.edit_message_text(text="You selected English.")
        lang = "en"
    elif query.data == "option2":
        await query.edit_message_text(text="Sie haben Deutsch gewählt.")
        lang = "de"
    elif query.data == "option3":
        await query.edit_message_text(text="Вы выбрали русский.")
        lang = "ru"
    else:
        await query.edit_message_text(text="Unknown option selected.")
        return MENU
    return AWAITING_INPUT

# Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (lang == "en") or (lang is None):
        await update.message.reply_text("Please choose the 'stock' menu and type the name of the asset you're interested in. The bot will scout its sources to deliver an answer as accurately as possible")
    elif lang == "de":
        await update.message.reply_text("Bitte wählen Sie das 'stock'-Menü und geben Sie den Namen des Vermögenswerts ein, an dem Sie interessiert sind. Der Bot wird seine Quellen durchsuchen, um eine Antwort so genau wie möglich zu liefern")
    else:
        await update.message.reply_text("Пожалуйста, выберите меню 'stock' и введите название интересующего вас актива. Бот будет искать информацию в своих источниках, чтобы предоставить максимально точный ответ")

async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global lookingForStock
    lookingForStock = True

    if (lang == "en") or (lang is None):
        await update.message.reply_text("Type the name of the asset you're interested in")
    elif lang == "de":
        await update.message.reply_text("Geben Sie den Namen des Vermögenswerts ein, an dem Sie interessiert sind")
    else:
        await update.message.reply_text("Введите название интересующего вас актива")

#async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")


#Responses

def handle_response(text: str):
    processed: str = text.lower()
    
    global lookingForStock 
    if lookingForStock == True:
        lookingForStock = False
        ticker = text.upper()
        stock = yf.Ticker(ticker)
        data = stock.info.get('regularMarketPrice', None)
        if data is not None:
            if (lang == "en") or (lang is None):
                answer = f"{ticker} is trading for {data} $ on the NASDAQ"
            elif lang == "de":
                answer = f"{ticker} wird an der NASDAQ für {data} $ gehandelt"
            else:
                answer = f"{ticker} торгуется на NASDAQ по цене {data} $"
        else:
            if (lang == "en") or (lang is None):
                answer = f"Sorry, I couldn't find any information on {ticker}. Check your spelling or use the ticker symbol instead of the name of the asset"
            elif lang == "de":
                answer = f"Entschuldigung, ich konnte keine Informationen zu {ticker} finden. Überprüfen wie Sie es geschrieben haben oder verwenden Sie das Tickersymbol anstelle des Namens des Vermögenswerts"
            else:
                answer = f"Извините, я не смог найти информацию о {ticker}. Проверьте правильность написания или используйте тикер вместо названия актива"
        return answer

    
    #if "alert" in processed:
    #    return("Use the /alert command to set an alert")  
    #return("I don't understand your input. Use /help if you're struggling with something")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    logger.info(f"User ({update.message.chat.id}) in {message_type}: {text}")

    if not lookingForStock:
        return 
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    logger.info(f"Bot:, {response}")
    await update.message.reply_text(response)


def main():

    logger.info("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            MENU: [CallbackQueryHandler(button)],
            AWAITING_INPUT:[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stock", stock_command))
    #app.add_handler(CommandHandler("alert", alert_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    logger.info("Polling...")
    app.run_polling(poll_interval=5)

if __name__ == "__main__":
    main()

