from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yfinance as yf
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("API_TOKEN")
BOT_USERNAME = os.getenv("BOT_HANDLE")


lang = None

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply.text("Hello! I am Evenius, your bot for sourcing stock prices in real time. Please choose your language")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply.text("Please choose the 'stock' menu and type the name of the asset you're interested in. The bot will scout its sources to deliver an answer as accurately as possible")


async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply.text("Type the name of the asset you're interested in")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


#Responses

def handle_response(text: str):
    processed: str = text.lower()

    if "stock" in processed:
        return("Use the /stock command to check stock prices")
    
    if "alert" in processed:
        return("Use the /alert command to set an alert")  
    return("I don't understand your input. Use /help if you're struggling with something")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: {text}")
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print("Bot:", response )
    await update.message.reply_text(response)


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token("TOKEN").build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stock", stock_command))
    #app.add_handler(CommandHandler("alert", alert_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=5)

print("indent")


