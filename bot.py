import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. إعدادات النظام
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"

# سيرفر وهمي لضمان استقرار Render
def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# 2. القوائم
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎮 أفضل 20 لعبة PSP (شغالة 100%)", callback_data='games_menu')],
        [InlineKeyboardButton("📚 تعليمات التشغيل", callback_data='help_menu')],
        [InlineKeyboardButton("🛠️ المطور", callback_data='dev')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # قائمة الـ 20 لعبة الأكثر طلباً وتحميلاً
    keyboard = [
        [InlineKeyboardButton("1. God of War: Ghost of Sparta", url="https://romspure.cc/roms/sony-playstation-portable/god-of-war-ghost-of-sparta")],
        [InlineKeyboardButton("2. GTA: Vice City Stories", url="https://romspure.cc/roms/sony-playstation-portable/grand-theft-auto-vice-city-stories")],
        [InlineKeyboardButton("3. Naruto Shippuden: Impact", url="https://romspure.cc/roms/sony-playstation-portable/naruto-shippuden-ultimate-ninja-impact")],
        [InlineKeyboardButton("4. Tekken 6", url="https://romspure.cc/roms/sony-playstation-portable/tekken-6")],
        [InlineKeyboardButton("5. Dragon Ball Z: Shin Budokai", url="https://romspure.cc/roms/sony-playstation-portable/dragon-ball-z-shin-budokai")],
        [InlineKeyboardButton("6. PES 2014 (Pro Evolution)", url="https://romspure.cc/roms/sony-playstation-portable/pro-evolution-soccer-2014")],
        [InlineKeyboardButton("7. Assassin's Creed: Bloodlines", url="https://romspure.cc/roms/sony-playstation-portable/assassins-creed-bloodlines")],
        [InlineKeyboardButton("8. Need for Speed: Most Wanted", url="https://romspure.cc/roms/sony-playstation-portable/need-for-speed-most-wanted-5-1-0")],
        [InlineKeyboardButton("9. Call of Duty: Roads to Victory", url="https://romspure.cc/roms/sony-playstation-portable/call-of-duty-roads-to-victory")],
        [InlineKeyboardButton("10. Ben 10: Protector of Earth", url="https://romspure.cc/roms/sony-playstation-portable/ben-10-protector-of-earth")],
        [InlineKeyboardButton("11. Spider-Man 3", url="https://romspure.cc/roms/sony-playstation-portable/spider-man-3")],
        [InlineKeyboardButton("12. FIFA 14", url="https://romspure.cc/roms/sony-playstation-portable/fifa-14-legacy-edition")],
        [InlineKeyboardButton("13. Mortal Kombat: Unchained", url="https://romspure.cc/roms/sony-playstation-portable/mortal-kombat-unchained")],
        [InlineKeyboardButton("14. WWE SmackDown vs Raw 2011", url="https://romspure.cc/roms/sony-playstation-portable/wwe-smackdown-vs-raw-2011")],
        [InlineKeyboardButton("15. Resident Evil: Director's Cut", url="https://romspure.cc/roms/sony-playstation-portable/resident-evil-directors-cut")],
        [InlineKeyboardButton("16. Crash Tag Team Racing", url="https://romspure.cc/roms/sony-playstation-portable/crash-tag-team-racing")],
        [InlineKeyboardButton("17. Metal Gear Solid: Peace Walker", url="https://romspure.cc/roms/sony-playstation-portable/metal-gear-solid-peace-walker")],
        [InlineKeyboardButton("18. Toy Story 3", url="https://romspure.cc/roms/sony-playstation-portable/toy-story-3")],
        [InlineKeyboardButton("19. Iron Man 2", url="https://romspure.cc/roms/sony-playstation-portable/iron-man-2")],
        [InlineKeyboardButton("20. Sonic Rivals", url="https://romspure.cc/roms/sony-playstation-portable/sonic-rivals")],
        [InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 أهلاً بك في نظام Swim-Core V5.9\n"
        "تم توفير أقوى 20 لعبة PSP بروابط صفحات رسمية مضمونة.",
        reply_markup=main_menu_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ قائمة الأساطير (التحميل مباشر من الصفحة):", reply_markup=games_menu_keyboard())
    
    elif query.data == 'help_menu':
        help_text = (
            "📚 **دليل تشغيل الألعاب:**\n\n"
            "1️⃣ اضغط على اللعبة لفتح صفحة التحميل.\n"
            "2️⃣ اضغط على زر **Download** داخل الموقع.\n"
            "3️⃣ بعد التحميل، استخدم **ZArchiver** لفك ضغط الملف.\n"
            "4️⃣ انقل الملف (ISO) إلى مجلد ألعابك.\n"
            "5️⃣ افتح تطبيق **PPSSPP** وابدأ اللعب!"
        )
        await query.edit_message_text(text=help_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))

    elif query.data == 'dev':
        await query.edit_message_text(text="👤 المطور: القائد سويم\n💻 @Swim_Architect", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))

    elif query.data == 'back_to_main':
        await query.edit_message_text(text="القائمة الرئيسية:", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)
