from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت يعمل!")

app = Application.builder().token("ضع_التوكن_هنا").build()

app.add_handler(CommandHandler("start", start))

app.run_polling()