import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات
logging.basicConfig(level=logging.INFO)

TOKEN = "PUT_YOUR_NEW_TOKEN_HERE"
OWNER_ID = 8078183906 

# سيرفر وهمي
def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# القائمة الرئيسية
def main_menu(user_id):
    row1 = [InlineKeyboardButton("🛠️ هوية المطور", callback_data='v3_final_dev')]
    
    if user_id == OWNER_ID:
        row1.append(InlineKeyboardButton("📡 حالة النظام", callback_data='v3_final_sys'))
    
    keyboard = [
        row1,
        [InlineKeyboardButton("🎮 مكتبة الألعاب", callback_data='v3_final_games')],
        [InlineKeyboardButton("📲 التطبيقات", callback_data='v3_final_apps')],
        [InlineKeyboardButton("📚 التعليمات", callback_data='v3_final_help')]
    ]
    return InlineKeyboardMarkup(keyboard)

# المعالج
async def handle_v3_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id

    try:
        await query.answer()
    except Exception as e:
        logging.error(e)

    if query.data == 'v3_final_dev':
        dev_text = """👤 **الاسم:** القائد سويم (Architect)
📡 **للتواصل:** @Swim_Architect
🛡️ *الإصدار: V3.0 Gold*"""
        
        await query.edit_message_text(
            dev_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 عودة", callback_data='v3_final_home')]
            ])
        )

    elif query.data == 'v3_final_games':
        games = [
            ("God of War", "god-of-war-ghost-of-sparta"),
            ("GTA: Vice City", "grand-theft-auto-vice-city-stories"),
            ("Naruto Impact", "naruto-shippuden-ultimate-ninja-impact"),
            ("Tekken 6", "tekken-6")
        ]

        kb = [
            [InlineKeyboardButton(f"🕹️ {g[0]}", url=f"https://romspure.cc/roms/sony-playstation-portable/{g[1]}")]
            for g in games
        ]

        kb.append([InlineKeyboardButton("🔙 عودة", callback_data='v3_final_home')])

        await query.edit_message_text(
            "🕹️ **مكتبة الألعاب:**",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(kb)
        )

    elif query.data == 'v3_final_apps':
        await query.edit_message_text(
            "📲 قسم التطبيقات قيد التطوير...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 عودة", callback_data='v3_final_home')]
            ])
        )

    elif query.data == 'v3_final_help':
        await query.edit_message_text(
            "📚 استخدم الأزرار للتنقل داخل البوت بسهولة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 عودة", callback_data='v3_final_home')]
            ])
        )

    elif query.data == 'v3_final_sys' and uid == OWNER_ID:
        await query.edit_message_text(
            "📡 النظام يعمل بشكل طبيعي.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 عودة", callback_data='v3_final_home')]
            ])
        )

    elif query.data == 'v3_final_home':
        await query.edit_message_text(
            "🏠 القائمة الرئيسية:",
            reply_markup=main_menu(uid)
        )

# أمر start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **Swim Core V3.0 Gold**\nنشط الآن!",
        parse_mode='Markdown',
        reply_markup=main_menu(update.message.from_user.id)
    )

# تشغيل
if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_v3_final))

    app.run_polling(drop_pending_updates=True)