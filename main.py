from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    Application, 
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    ContextTypes, 
    CallbackQueryHandler,
    JobQueue
)
import yfinance as yf
import matplotlib.pyplot as plt
import os
import logging
import io
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("API_TOKEN")
BOT_USERNAME = os.getenv("BOT_HANDLE")
MENU, AWAITING_INPUT, AWAITING_ALERT = range(3)


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
    lang = context.user_data.get("lang")
    if (lang == "en") or (lang is None):
        await update.message.reply_text("Please choose the 'stock' menu and type the name of the asset you're interested in. The bot will scout its sources to deliver an answer as accurately as possible")
    elif lang == "de":
        await update.message.reply_text("Bitte wählen Sie das 'stock'-Menü und geben Sie den Namen des Vermögenswerts ein, an dem Sie interessiert sind. Der Bot wird seine Quellen durchsuchen, um eine Antwort so genau wie möglich zu liefern")
    else:
        await update.message.reply_text("Пожалуйста, выберите меню 'stock' и введите название интересующего вас актива. Бот будет искать информацию в своих источниках, чтобы предоставить максимально точный ответ")

async def stock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["lookingForStock"] = True
    lang = context.user_data.get("lang")

    if (lang == "en") or (lang is None):
        await update.message.reply_text("Type the name of the asset you're interested in")
    elif lang == "de":
        await update.message.reply_text("Geben Sie den Namen des Vermögenswerts ein, an dem Sie interessiert sind")
    else:
        await update.message.reply_text("Введите название интересующего вас актива")
    return AWAITING_INPUT

async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["settingAlert"] = True
    lang = context.user_data.get("lang")
    if (lang == "en") or (lang is None):
        await update.message.reply_text("Type the name of the desired asset in the form 'Ticker Price', e.g. 'TSLA 200'. The bot will recheck the price and send you an alert when the desired price is reached")
    elif lang == "de":
        await update.message.reply_text("Geben Sie den Namen des gewünschten Vermögenswerts in der Form 'Ticker Preis' ein, z.B. 'TSLA 200'. Der Bot wird den Preis erneut überprüfen und Ihnen eine Benachrichtigung senden, wenn der gewünschte Preis erreicht ist")
    else:
        await update.message.reply_text("Введите название желаемого актива в форме 'Тикер Цена', например 'TSLA 200'. Бот будет проверять цену и отправит Вам уведомление, когда будет достигнута желаемая цена")
    return AWAITING_ALERT



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")


#Responses

async def check_alert(context: ContextTypes.DEFAULT_TYPE):

    job_data = context.job.data
    jobAlertName = job_data["alertName"]
    jobAlertPrice = job_data["alertPrice"]
    chat_id = job_data["chat_id"]
    lang = job_data["lang"]
    job_data["checks"] += 1
    if job_data["checks"] >= 44640:
        if (lang == "en") or (lang is None):
            alertText = f"Alert for {jobAlertName} at {jobAlertPrice} $ expired after 31 days without reaching the desired price"
        elif lang == "de":
            alertText = f"Benachrichtigung für {jobAlertName} bei {jobAlertPrice} $ ist nach 31 Tagen ohne Erreichen des gewünschten Preises abgelaufen"
        else:
            alertText = f"Напоминание для {jobAlertName} при {jobAlertPrice} $ истекло после 31 дня без достижения желаемой цены"
        await context.bot.send_message(chat_id=chat_id, text=alertText)
        context.job.schedule_removal()
        return
    stockName = yf.Ticker(jobAlertName)
    data = stockName.info.get("regularMarketPrice", None)
    if (data is not None) and (data >= jobAlertPrice) and (jobAlertPrice > 0):
        if (lang == "en") or (lang is None):
            alertText = f"{jobAlertName} reached the price of {jobAlertPrice} $"
        elif lang == "de":
            alertText = f"{jobAlertName} hat den Preis von {jobAlertPrice} $ erreicht"
        else:
            alertText = f"{jobAlertName} достиг цены в {jobAlertPrice} $" 
        await context.bot.send_message(chat_id=chat_id, text=alertText)
        context.job.schedule_removal()


def handle_response(text: str, context: ContextTypes.DEFAULT_TYPE =None, chat_id=None):
    processed: str = text.lower()
    
    lang = context.user_data.get("lang")

    if context.user_data.get("settingAlert"):
        context.user_data["settingAlert"] = False

    if settingAlert == True:
        settingAlert = False
        tickerAlert = text.upper().split()
        alertName = tickerAlert[0]
        try:
            alertPrice = float(tickerAlert[1])
        except (IndexError, ValueError):
            return "Use the format 'TICKER PRICE', e.g. 'TSLA 200'"
        context.job_queue.run_repeating(
            check_alert,
            interval=60,
            data={"alertName": alertName, "alertPrice": alertPrice, "chat_id": chat_id, "checks": 0, "lang": lang}
        )
        return f"Alert set for {alertName} at ${alertPrice}"

    if context.user_data.get("lookingForStock"):
        context.user_data["lookingForStock"] = False
        ticker = text.upper()
        stock = yf.Ticker(ticker)
        data = stock.info.get('regularMarketPrice', None)
        if data is not None:
            if (lang == "en") or (lang is None):
                answer = f"{ticker} is trading for {data} $ on the NASDAQ. Use /stock again to check another asset"
            elif lang == "de":
                answer = f"{ticker} wird an der NASDAQ für {data} $ gehandelt. Verwenden Sie /stock nochmal, um einen anderen Vermögenswert zu überprüfen"
            else:
                answer = f"{ticker} торгуется на NASDAQ по цене {data} $. Используйте /stock снова, чтобы проверить другой актив"   
            buf = generate_chart(ticker, lang)
            return buf, answer
        else:
            if (lang == "en") or (lang is None):
                answer = f"Sorry, I couldn't find any information on {ticker}. Check your spelling or use the ticker symbol instead of the name of the asset"
            elif lang == "de":
                answer = f"Entschuldigung, ich konnte keine Informationen zu {ticker} finden. Überprüfen wie Sie es geschrieben haben oder verwenden Sie das Tickersymbol anstelle des Namens des Vermögenswerts"
            else:
                answer = f"Извините, я не смог найти информацию о {ticker}. Проверьте правильность написания или используйте тикер вместо названия актива"
            return answer
             

def generate_chart(ticker: str, lang: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['Close'])
    
    if lang == "en" or lang is None:
        plt.title(f"{ticker} in the last 30 Days")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
    elif lang == "de":
        plt.title(f"{ticker} in den letzten 30 Tagen")
        plt.xlabel("Datum")
        plt.ylabel("Preis ($)")
    else:
        plt.title(f"{ticker} за последние 30 дней")
        plt.xlabel("Дата")
        plt.ylabel("Цена ($)")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    logger.info(f"User ({update.message.chat.id}) in {message_type}: {text}")

    if not context.user_data.get("lookingForStock") and not context.user_data.get("settingAlert"):
        return 
    if message_type == "group":
        if BOT_USERNAME in text:
            text: str = text.replace(BOT_USERNAME, "").strip()
        else:
            return
    response = handle_response(text, context, update.message.chat_id)

    if isinstance(response, tuple):
        buf, answer = response
        await update.message.reply_photo(photo=InputFile(buf))
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text(response)   


def main():

    logger.info("Starting bot...")
    app = Application.builder().token(TOKEN).job_queue(JobQueue()).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            CommandHandler("stock", stock_command),
            CommandHandler("alert", alert_command),
        ],
        states={
            MENU: [CallbackQueryHandler(button)],
            AWAITING_INPUT:
            [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
                CommandHandler("stock", stock_command),
                CommandHandler("alert", alert_command),
                CommandHandler("help", help_command),
            ],
            AWAITING_ALERT:            [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
                CommandHandler("stock", stock_command),
                CommandHandler("alert", alert_command),
                CommandHandler("help", help_command),
            ],
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    app.add_handler(conv_handler)

    app.add_error_handler(error)

    logger.info("Polling...")
    app.run_polling(poll_interval=5)

if __name__ == "__main__":
    main()

