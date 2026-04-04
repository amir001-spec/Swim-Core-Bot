import logging
import os
import http.server
import socketserver
import threading
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. إعدادات النخبة والأمان
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"
OWNER_ID = 8078183906 

def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# 2. هندسة الواجهة (تطابق الصور 100%)
def main_menu_keyboard(user_id):
    # الصف الأول: الهوية وحالة النظام (للمالك فقط)
    top_row = [InlineKeyboardButton("🛠️ هوية المطور", callback_data='dev_info')]
    if user_id == OWNER_ID:
        top_row.append(InlineKeyboardButton("📡 حالة النظام", callback_data='sys_status'))
    
    keyboard = [
        top_row,
        [InlineKeyboardButton("🎮 مكتبة الألعاب المضمونة", callback_data='games_menu')],
        [InlineKeyboardButton("📲 تطبيقات مهكرة (15 تطبيق)", callback_data='apps_menu')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='help_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def apps_menu_keyboard():
    # روابط مباشرة ومفحوصة (LiteAPKs و APKMody)
    keyboard = [
        [InlineKeyboardButton("🎵 Spotify Premium", url="https://apkmody.com/apps/spotify-music")],
        [InlineKeyboardButton("📸 PicsArt Gold", url="https://apkpure.com/picsart-ai-photo-video-editor/com.picsart.studio")],
        [InlineKeyboardButton("🎬 CapCut Pro", url="https://apkmody.com/apps/capcut")],
        [InlineKeyboardButton("📺 YouTube ReVanced", url="https://revanced.net/download-revanced-apk")],
        [InlineKeyboardButton("🛡️ Kaspersky Pro", url="https://apkpure.com/kaspersky-antivirus-vpn-app/com.kms.free")],
        [InlineKeyboardButton("📥 SnapTube VIP", url="https://www.snaptube.com/")],
        [InlineKeyboardButton("🎨 Canva Pro", url="https://apkmody.com/apps/canva")],
        [InlineKeyboardButton("📂 ZArchiver Pro", url="https://apkpure.com/zarchiver/ru.zdevs.zarchiver")],
        [InlineKeyboardButton("🎥 InShot Pro", url="https://apkmody.com/apps/inshot")],
        [InlineKeyboardButton("🌀 Truecaller Gold", url="https://apkmody.com/apps/truecaller")],
        [InlineKeyboardButton("🎞️ Netflix Premium", url="https://liteapks.com/netflix.html")],
        [InlineKeyboardButton("📱 TikTok Mod", url="https://liteapks.com/tiktok.html")],
        [InlineKeyboardButton("🎮 Minecraft PE", url="https://liteapks.com/minecraft.html")],
        [InlineKeyboardButton("🧹 CCleaner Pro", url="https://apkmody.com/apps/ccleaner")],
        [InlineKeyboardButton("🗝️ ExpressVPN", url="https://liteapks.com/expressvpn.html")],
        [InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # الـ 30 لعبة PSP (بدون تغيير)
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
        [InlineKeyboardButton("21. Prince of Persia", url="https://romspure.cc/roms/sony-playstation-portable/prince-of-persia-rival-swords")],
        [InlineKeyboardButton("22. Midnight Club 3", url="https://romspure.cc/roms/sony-playstation-portable/midnight-club-3-dub-edition")],
        [InlineKeyboardButton("23. Dragon Ball Z: Tenkaichi", url="https://romspure.cc/roms/sony-playstation-portable/dragon-ball-z-tenkaichi-tag-team")],
        [InlineKeyboardButton("24. Manhunt 2", url="https://romspure.cc/roms/sony-playstation-portable/manhunt-2")],
        [InlineKeyboardButton("25. Ghost Rider", url="https://romspure.cc/roms/sony-playstation-portable/ghost-rider")],
        [InlineKeyboardButton("26. Resistance", url="https://romspure.cc/roms/sony-playstation-portable/resistance-retribution")],
        [InlineKeyboardButton("27. Silent Hill", url="https://romspure.cc/roms/sony-playstation-portable/silent-hill-origins")],
        [InlineKeyboardButton("28. Dante's Inferno", url="https://romspure.cc/roms/sony-playstation-portable/dantes-inferno")],
        [InlineKeyboardButton("29. Burnout Legends", url="https://romspure.cc/roms/sony-playstation-portable/burnout-legends")],
        [InlineKeyboardButton("30. LEGO Batman", url="https://romspure.cc/roms/sony-playstation-portable/lego-batman-the-videogame")],
        [InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data='back_home')]
    ]
    return InlineKeyboardMarkup(keyboard)

# 3. معالجة العمليات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    name = update.message.from_user.first_name
    welcome = f"🚀 **نظام Swim Core V7.2 المحدث جاهز الآن!**\nتم حل مشكلة التضارب وتحديث الروابط."
    await update.message.reply_text(welcome, parse_mode='Markdown', reply_markup=main_menu_keyboard(uid))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ **مكتبة الألعاب (30 لعبة):**", parse_mode='Markdown', reply_markup=games_menu_keyboard())
    
    elif query.data == 'apps_menu':
        await query.edit_message_text(text="📲 **تطبيقات مهكرة (15 تطبيق):**", parse_mode='Markdown', reply_markup=apps_menu_keyboard())
    
    elif query.data == 'dev_info':
        dev_text = "🎖️ **هوية المطور:**\n👤 الاسم: القائد سويم (Architect)\n📡 التواصل: @Swim_Architect\n🛡️ جميع الحقوق محفوظة لـ Swim-Core."
        await query.edit_message_text(text=dev_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))
    
    elif query.data == 'sys_status' and uid == OWNER_ID:
        status = "📡 **حالة النظام:**\n✅ السيرفر: مستقر\n✅ الألعاب: 30\n✅ التطبيقات: 15"
        await query.edit_message_text(text=status, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    elif query.data == 'help_menu':
        help_full = (
            "📚 **دليل الاستخدام:**\n\n"
            "1️⃣ **للألعاب:** حمل الملف، فك الضغط بـ **ZArchiver**، وشغله بـ **PPSSPP**.\n"
            "2️⃣ **للتطبيقات:** حمل الـ APK وثبته مباشرة.\n\n"
            "⚠️ الروابط محدثة ومفحوصة."
        )
        await query.edit_message_text(text=help_full, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    elif query.data == 'back_home':
        await query.edit_message_text(text="القائمة الرئيسية للتحكم:", reply_markup=main_menu_keyboard(uid))

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # أهم سطر لحل مشكلة التضارب (Conflict)
    app.run_polling(drop_pending_updates=True, close_loop=False)
