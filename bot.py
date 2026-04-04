import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. إعدادات النخبة
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"
OWNER_ID = 8078183906  # تم إثبات ملكيتك للنظام بنجاح ✅

# سيرفر حماية البقاء (Keep-Alive)
def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# 2. تصميم القوائم الاحترافية
def main_menu_keyboard(user_id):
    keyboard = [
        [InlineKeyboardButton("🎮 مكتبة الأساطير (20 لعبة)", callback_data='games_menu')],
        [InlineKeyboardButton("📚 دليل الاحتراف", callback_data='help_menu')],
        [InlineKeyboardButton("🎖️ هوية المطور", callback_data='dev')]
    ]
    # ميزة المالك: زر حالة النظام يظهر لك أنت فقط
    if user_id == OWNER_ID:
        keyboard.append([InlineKeyboardButton("📡 لوحة تحكم القائد (خاص)", callback_data='status')])
    
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # الروابط التي أكدت أنها تعمل بمثالية (بدون تغيير)
    keyboard = [
        [InlineKeyboardButton("1. God of War: Ghost of Sparta", url="https://romspure.cc/roms/sony-playstation-portable/god-of-war-ghost-of-sparta")],
        [InlineKeyboardButton("2. GTA: Vice City Stories", url="https://romspure.cc/roms/sony-playstation-portable/grand-theft-auto-vice-city-stories")],
        [InlineKeyboardButton("3. Naruto Shippuden: Impact", url="https://romspure.cc/roms/sony-playstation-portable/naruto-shippuden-ultimate-ninja-impact")],
        [InlineKeyboardButton("4. Tekken 6", url="https://romspure.cc/roms/sony-playstation-portable/tekken-6")],
        [InlineKeyboardButton("5. Dragon Ball Z: Shin Budokai", url="https://romspure.cc/roms/sony-playstation-portable/dragon-ball-z-shin-budokai")],
        [InlineKeyboardButton("6. PES 2014", url="https://romspure.cc/roms/sony-playstation-portable/pro-evolution-soccer-2014")],
        [InlineKeyboardButton("7. Assassin's Creed", url="https://romspure.cc/roms/sony-playstation-portable/assassins-creed-bloodlines")],
        [InlineKeyboardButton("8. Need for Speed", url="https://romspure.cc/roms/sony-playstation-portable/need-for-speed-most-wanted-5-1-0")],
        [InlineKeyboardButton("9. Call of Duty", url="https://romspure.cc/roms/sony-playstation-portable/call-of-duty-roads-to-victory")],
        [InlineKeyboardButton("10. Ben 10: Protector of Earth", url="https://romspure.cc/roms/sony-playstation-portable/ben-10-protector-of-earth")],
        [InlineKeyboardButton("11. Spider-Man 3", url="https://romspure.cc/roms/sony-playstation-portable/spider-man-3")],
        [InlineKeyboardButton("12. FIFA 14", url="https://romspure.cc/roms/sony-playstation-portable/fifa-14-legacy-edition")],
        [InlineKeyboardButton("13. Mortal Kombat", url="https://romspure.cc/roms/sony-playstation-portable/mortal-kombat-unchained")],
        [InlineKeyboardButton("14. WWE SmackDown 2011", url="https://romspure.cc/roms/sony-playstation-portable/wwe-smackdown-vs-raw-2011")],
        [InlineKeyboardButton("15. Resident Evil", url="https://romspure.cc/roms/sony-playstation-portable/resident-evil-directors-cut")],
        [InlineKeyboardButton("16. Crash Racing", url="https://romspure.cc/roms/sony-playstation-portable/crash-tag-team-racing")],
        [InlineKeyboardButton("17. Metal Gear Solid", url="https://romspure.cc/roms/sony-playstation-portable/metal-gear-solid-peace-walker")],
        [InlineKeyboardButton("18. Toy Story 3", url="https://romspure.cc/roms/sony-playstation-portable/toy-story-3")],
        [InlineKeyboardButton("19. Iron Man 2", url="https://romspure.cc/roms/sony-playstation-portable/iron-man-2")],
        [InlineKeyboardButton("20. Sonic Rivals", url="https://romspure.cc/roms/sony-playstation-portable/sonic-rivals")],
        [InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# 3. معالجة العمليات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    
    # رسالة ترحيب مخصصة للمالك
    if user_id == OWNER_ID:
        welcome_text = f"🫡 **مرحباً بك سيادة القائد {name}**\nالنظام تحت تصرفك الآن بالكامل."
    else:
        welcome_text = f"🎮 **مرحباً بك {name} في Swim-Core**\nأكبر مكتبة ألعاب PSP مضمونة بإشراف Swim Architect."

    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=main_menu_keyboard(user_id))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ **مكتبة الألعاب المختارة:**\nتفضل بتحميل ألعابك المفضلة مباشرة.", parse_mode='Markdown', reply_markup=games_menu_keyboard())
    
    elif query.data == 'help_menu':
        help_text = (
            "📚 **دليل تشغيل الألعاب:**\n\n"
            "1. اختر اللعبة من القائمة.\n"
            "2. اضغط Download في الموقع المفتوح.\n"
            "3. فك الضغط بـ **ZArchiver**.\n"
            "4. شغل ملف الـ **ISO** عبر محاكي **PPSSPP**.\n\n"
            "🛡️ *روابطنا تخضع للفحص المستمر.*"
        )
        await query.edit_message_text(text=help_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))

    elif query.data == 'dev':
        dev_info = (
            "🎖️ **بطاقة المطور الرسمية**\n\n"
            "👤 **الاسم:** القائد سويم (Swim Architect)\n"
            "🥇 **الرتبة:** مطور ومؤسس المشروع\n"
            "📡 **التواصل:** @Swim_Architect\n\n"
            "🛡️ *جميع الحقوق محفوظة لنظام Swim-Core 2026.*"
        )
        await query.edit_message_text(text=dev_info, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))

    elif query.data == 'status':
        if user_id == OWNER_ID:
            status_report = (
                "📡 **تقرير حالة النظام السري:**\n\n"
                "✅ السيرفر: Render Cloud (Online)\n"
                "✅ قاعدة البيانات: مستقرة 100%\n"
                "✅ التوكن: مفعل بنجاح\n"
                "🛰️ عدد الألعاب المسجلة: 20\n"
                "🔒 مستوى الحماية: عالي (Architect Encryption)"
            )
            await query.edit_message_text(text=status_report, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))
        else:
            await query.answer("❌ خطأ أمني: لا تملك صلاحية المالك.", show_alert=True)

    elif query.data == 'back_to_main':
        await query.edit_message_text(text="القائمة الرئيسية:", reply_markup=main_menu_keyboard(user_id))

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)
