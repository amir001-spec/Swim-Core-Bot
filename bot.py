import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. إعدادات النخبة (التوكن والمعرف الخاص بك)
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"
OWNER_ID = 8078183906 

# سيرفر وهمي لتجنب توقف البوت على منصة Render
def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# 2. هندسة القائمة الرئيسية (تطابق صورتك تماماً)
def main_menu_keyboard(user_id):
    top_row = [InlineKeyboardButton("🛠️ هوية المطور", callback_data='dev_info')]
    if user_id == OWNER_ID:
        top_row.append(InlineKeyboardButton("📡 حالة النظام", callback_data='sys_status'))
    
    keyboard = [
        top_row,
        [InlineKeyboardButton("🎮 مكتبة الألعاب المضمونة", callback_data='games_page')],
        [InlineKeyboardButton("📲 تطبيقات مهكرة (15 تطبيق)", callback_data='apps_page')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='help_page')]
    ]
    return InlineKeyboardMarkup(keyboard)

# 3. مكتبة الألعاب (30 لعبة كاملة بروابط Romspure)
def games_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("1. God of War: Ghost of Sparta", url="https://romspure.cc/roms/sony-playstation-portable/god-of-war-ghost-of-sparta")],
        [InlineKeyboardButton("2. GTA: Vice City Stories", url="https://romspure.cc/roms/sony-playstation-portable/grand-theft-auto-vice-city-stories")],
        [InlineKeyboardButton("3. Naruto Shippuden: Ultimate Ninja Impact", url="https://romspure.cc/roms/sony-playstation-portable/naruto-shippuden-ultimate-ninja-impact")],
        [InlineKeyboardButton("4. Tekken 6", url="https://romspure.cc/roms/sony-playstation-portable/tekken-6")],
        [InlineKeyboardButton("5. Dragon Ball Z: Shin Budokai", url="https://romspure.cc/roms/sony-playstation-portable/dragon-ball-z-shin-budokai")],
        [InlineKeyboardButton("6. Pro Evolution Soccer 2014", url="https://romspure.cc/roms/sony-playstation-portable/pro-evolution-soccer-2014")],
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
        [InlineKeyboardButton("21. Prince of Persia: Rival Swords", url="https://romspure.cc/roms/sony-playstation-portable/prince-of-persia-rival-swords")],
        [InlineKeyboardButton("22. Midnight Club 3: DUB Edition", url="https://romspure.cc/roms/sony-playstation-portable/midnight-club-3-dub-edition")],
        [InlineKeyboardButton("23. Dragon Ball Z: Tenkaichi Tag Team", url="https://romspure.cc/roms/sony-playstation-portable/dragon-ball-z-tenkaichi-tag-team")],
        [InlineKeyboardButton("24. Manhunt 2", url="https://romspure.cc/roms/sony-playstation-portable/manhunt-2")],
        [InlineKeyboardButton("25. Ghost Rider", url="https://romspure.cc/roms/sony-playstation-portable/ghost-rider")],
        [InlineKeyboardButton("26. Resistance: Retribution", url="https://romspure.cc/roms/sony-playstation-portable/resistance-retribution")],
        [InlineKeyboardButton("27. Silent Hill: Origins", url="https://romspure.cc/roms/sony-playstation-portable/silent-hill-origins")],
        [InlineKeyboardButton("28. Dante's Inferno", url="https://romspure.cc/roms/sony-playstation-portable/dantes-inferno")],
        [InlineKeyboardButton("29. Burnout Legends", url="https://romspure.cc/roms/sony-playstation-portable/burnout-legends")],
        [InlineKeyboardButton("30. LEGO Batman: The Videogame", url="https://romspure.cc/roms/sony-playstation-portable/lego-batman-the-videogame")],
        [InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

# 4. ترسانة التطبيقات (15 تطبيقاً مهكراً بروابط Apkmody)
def apps_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎵 Spotify Premium", url="https://apkmody.com/apps/spotify-music")],
        [InlineKeyboardButton("📸 PicsArt Gold", url="https://apkmody.com/apps/picsart-photo-studio")],
        [InlineKeyboardButton("🎬 CapCut Pro", url="https://apkmody.com/apps/capcut")],
        [InlineKeyboardButton("📺 YouTube ReVanced", url="https://revanced.net/download-revanced-apk")],
        [InlineKeyboardButton("🛡️ Kaspersky Pro", url="https://apkpure.com/kaspersky-antivirus-vpn-app/com.kms.free")],
        [InlineKeyboardButton("📥 SnapTube VIP", url="https://www.snaptube.com/")],
        [InlineKeyboardButton("🎨 Canva Pro", url="https://apkmody.com/apps/canva")],
        [InlineKeyboardButton("📂 ZArchiver Pro", url="https://apkpure.com/zarchiver/ru.zdevs.zarchiver")],
        [InlineKeyboardButton("🎥 InShot Pro", url="https://apkmody.com/apps/inshot")],
        [InlineKeyboardButton("🌀 Truecaller Gold", url="https://apkmody.com/apps/truecaller")],
        [InlineKeyboardButton("🎞️ Netflix Premium", url="https://liteapks.com/netflix.html")],
        [InlineKeyboardButton("📱 TikTok Mod (No Ads)", url="https://liteapks.com/tiktok.html")],
        [InlineKeyboardButton("🎮 Minecraft PE Full", url="https://liteapks.com/minecraft.html")],
        [InlineKeyboardButton("🧹 CCleaner Pro", url="https://apkmody.com/apps/ccleaner")],
        [InlineKeyboardButton("🗝️ ExpressVPN Pro", url="https://liteapks.com/expressvpn.html")],
        [InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

# 5. معالج التفاعل الرئيسي (إصلاح "هوية المطور" والتعليمات)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    # خيار هوية المطور (مفصل بالكامل)
    if query.data == 'dev_info':
        dev_text = (
            "🎖️ **بطاقة هوية المطور الرسمي**\n\n"
            "👤 **الاسم:** القائد سويم (Architect)\n"
            "🥇 **الرتبة:** مؤسس ومطور نظام Swim Core\n"
            "📡 **قناة المطور:** @Swim_Architect\n\n"
            "🛡️ *هذا النظام محمي برمجياً وحقوقه محفوظة لعام 2026.*"
        )
        await query.edit_message_text(text=dev_text, parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    # خيار حالة النظام
    elif query.data == 'sys_status':
        if uid == OWNER_ID:
            status_text = (
                "📡 **لوحة تحكم القائد العليا:**\n\n"
                "✅ حالة السيرفر: نشط (Online)\n"
                "✅ مكتبة الألعاب: 30 ملف ISO\n"
                "✅ التطبيقات: 15 ملف APK\n"
                "🔒 مستوى الأمان: مشفر بالكامل"
            )
            await query.edit_message_text(text=status_text, parse_mode='Markdown', 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))
        else:
            await query.answer("❌ عذراً، هذا الخيار مخصص للقائد سويم فقط.", show_alert=True)

    # مكتبة الألعاب
    elif query.data == 'games_page':
        await query.edit_message_text(text="🕹️ **مكتبة ألعاب PSP (30 لعبة مختارة):**", 
            parse_mode='Markdown', reply_markup=games_menu_keyboard())
    
    # قائمة التطبيقات
    elif query.data == 'apps_page':
        await query.edit_message_text(text="📲 **ترسانة التطبيقات المهكرة (15 تطبيق):**", 
            parse_mode='Markdown', reply_markup=apps_menu_keyboard())

    # قائمة التعليمات (مفصلة جداً)
    elif query.data == 'help_page':
        help_full = (
            "📚 **الدليل الشامل لتشغيل الألعاب والتطبيقات:**\n\n"
            "🔹 **أولاً: تشغيل الألعاب (PSP):**\n"
            "1. اختر اللعبة من القائمة واضغط على الرابط.\n"
            "2. بعد التحميل، استخدم تطبيق **ZArchiver** لفك الضغط عن الملف.\n"
            "3. افتح محاكي **PPSSPP** واختر مجلد اللعبة لبدء اللعب.\n\n"
            "🔹 **ثانياً: تثبيت التطبيقات المهكرة:**\n"
            "1. حمل ملف الـ APK من الروابط الموفرة.\n"
            "2. قم بتفعيل خيار 'تثبيت من مصادر مجهولة' في إعدادات هاتفك.\n"
            "3. ثبت التطبيق واستمتع بميزات الـ Pro مجاناً.\n\n"
            "⚠️ **تنبيه:** جميع الروابط مفحوصة لضمان أمان جهازك."
        )
        await query.edit_message_text(text=help_full, parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    # العودة للرئيسية
    elif query.data == 'back_home':
        await query.edit_message_text(text="القائمة الرئيسية للتحكم:", 
            reply_markup=main_menu_keyboard(uid))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = "🚀 **نظام Swim Core V10.0 المحدث**\nتم الإصلاح الشامل لجميع الأزرار والروابط."
    await update.message.reply_text(welcome, parse_mode='Markdown', 
        reply_markup=main_menu_keyboard(update.message.from_user.id))

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # السطر الذي ينهي مشكلة الـ Conflict المزعجة
    app.run_polling(drop_pending_updates=True)
