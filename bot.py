import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 8078183906

# ✅ تحقق من التوكن
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN غير موجود! أضفه في Render Environment Variables")

# ✅ سيرفر محسن
def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            return

    with socketserver.TCPServer(("0.0.0.0", port), Handler) as httpd:
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

    elif query.data == 'sys' and