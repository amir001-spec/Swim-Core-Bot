import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات النظام
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"

# --- جزء "خداع" Render لفتح المنفذ المطلوب ---
def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"--- Dummy Server started at port {port} ---")
        httpd.serve_forever()

# --- بقية كود البوت ---
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎮 مكتبة ألعاب PSP المضمونة", callback_data='games_menu')],
        [InlineKeyboardButton("🛠️ المطور", callback_data='dev'), InlineKeyboardButton("📡 الحالة", callback_data='status')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("God of War", url="https://vimm.net/vault/23541")],
        [InlineKeyboardButton("GTA: Liberty City Stories", url="https://vimm.net/vault/23588")],
        [InlineKeyboardButton("Tekken 6", url="https://vimm.net/vault/24250")],
        [InlineKeyboardButton("🔍 تصفح آلاف الألعاب", url="https://vimm.net/vault/PSP")],
        [InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 نظام Swim Core V5.5 المحدث\nتم حل مشكلة الـ Port بنجاح!", reply_markup=main_menu_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ اختر اللعبة (سيرفرات Vimm المضمونة):", reply_markup=games_menu_keyboard())
    elif query.data == 'back_to_main':
        await query.edit_message_text(text="قائمة التحكم الرئيسية:", reply_markup=main_menu_keyboard())
    elif query.data == 'dev':
        await query.edit_message_text(text="👤 المطور: القائد سويم\n💻 @Swim_Architect", reply_markup=main_menu_keyboard())
    elif query.data == 'status':
        await query.edit_message_text(text="✅ النظام: متصل ومستقر V5.5", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    # تشغيل السيرفر الوهمي في الخلفية لإرضاء Render
    threading.Thread(target=start_dummy_server, daemon=True).start()
    
    # تشغيل البوت
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("--- SYSTEM V5.5 IS READY ---")
    app.run_polling(drop_pending_updates=True)
