import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

# 🔐 التوكن من البيئة (آمن)
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 8078183906

def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

def main_menu(user_id):
    row1 = [InlineKeyboardButton("🛠️ هوية المطور", callback_data='dev')]
    
    if user_id == OWNER_ID:
        row1.append(InlineKeyboardButton("📡 حالة النظام", callback_data='sys'))
    
    keyboard = [
        row1,
        [InlineKeyboardButton("🎮 مكتبة الألعاب", callback_data='games')],
        [InlineKeyboardButton("📲 التطبيقات", callback_data='apps')],
        [InlineKeyboardButton("📚 التعليمات", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id

    await query.answer()

    if query.data == 'dev':
        await query.edit_message_text(
            "👤 المطور: Swim Architect\n📡 @Swim_Architect",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='home')]])
        )

    elif query.data == 'games':
        await query.edit_message_text(
            "🎮 سيتم إضافة الألعاب لاحقًا",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='home')]])
        )

    elif query.data == 'apps':
        await query.edit_message_text(
            "📲 سيتم إضافة التطبيقات لاحقًا",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='home')]])
        )

    elif query.data == 'help':
        await query.edit_message_text(
            "📚 استخدم الأزرار للتنقل",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='home')]])
        )

    elif query.data == 'sys' and uid == OWNER_ID:
        await query.edit_message_text(
            "📡 البوت يعمل بشكل طبيعي",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data='home')]])
        )

    elif query.data == 'home':
        await query.edit_message_text(
            "🏠 القائمة الرئيسية",
            reply_markup=main_menu(uid)
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 البوت يعمل الآن",
        reply_markup=main_menu(update.message.from_user.id)
    )

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle))

    app.run_polling()