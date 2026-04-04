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
OWNER_ID = 8078183906  # هويتك كمالك مثبتة ✅

def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# 2. تصميم القوائم المتكاملة
def main_menu_keyboard(user_id):
    keyboard = [
        [InlineKeyboardButton("🎮 مكتبة الألعاب (30 لعبة)", callback_data='games_menu')],
        [InlineKeyboardButton("📲 تطبيقات مهكرة (Premium)", callback_data='apps_menu')],
        [InlineKeyboardButton("📚 دليل الاحتراف", callback_data='help_menu')],
        [InlineKeyboardButton("🎖️ هوية المطور", callback_data='dev')]
    ]
    if user_id == OWNER_ID:
        keyboard.append([InlineKeyboardButton("📡 لوحة تحكم القائد", callback_data='status')])
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # الـ 20 القديمة + 10 أساطير جديدة (بدون تغيير الروابط الأصلية)
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
        # الـ 10 الجديدة
        [InlineKeyboardButton("21. Prince of Persia: Rival Swords", url="https://romspure.cc/roms/sony-playstation-portable/prince-of-persia-rival-swords")],
        [InlineKeyboardButton("22. Midnight Club 3: DUB Edition", url="https://romspure.cc/roms/sony-playstation-portable/midnight-club-3-dub-edition")],
        [InlineKeyboardButton("23. Dragon Ball Z: Tenkaichi Tag", url="https://romspure.cc/roms/sony-playstation-portable/dragon-ball-z-tenkaichi-tag-team")],
        [InlineKeyboardButton("24. Manhunt 2", url="https://romspure.cc/roms/sony-playstation-portable/manhunt-2")],
        [InlineKeyboardButton("25. Ghost Rider", url="https://romspure.cc/roms/sony-playstation-portable/ghost-rider")],
        [InlineKeyboardButton("26. Resistance: Retribution", url="https://romspure.cc/roms/sony-playstation-portable/resistance-retribution")],
        [InlineKeyboardButton("27. Silent Hill: Origins", url="https://romspure.cc/roms/sony-playstation-portable/silent-hill-origins")],
        [InlineKeyboardButton("28. Dante's Inferno", url="https://romspure.cc/roms/sony-playstation-portable/dantes-inferno")],
        [InlineKeyboardButton("29. Burnout Legends", url="https://romspure.cc/roms/sony-playstation-portable/burnout-legends")],
        [InlineKeyboardButton("30. LEGO Batman", url="https://romspure.cc/roms/sony-playstation-portable/lego-batman-the-videogame")],
        [InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def apps_menu_keyboard():
    # قائمة الـ 10 تطبيقات المهكرة الأساسية
    keyboard = [
        [InlineKeyboardButton("🎵 Spotify Premium (بدون إعلانات)", url="https://m.happymod.com/spotify-music-mod/com.spotify.music/")],
        [InlineKeyboardButton("📸 PicsArt Gold (مفتوح بالكامل)", url="https://m.happymod.com/picsart-photo-studio-mod/com.picsart.studio/")],
        [InlineKeyboardButton("🎬 CapCut Pro (بدون علامة مائية)", url="https://m.happymod.com/capcut-video-editor-mod/com.lemon.lvoverseas/")],
        [InlineKeyboardButton("📺 YouTube ReVanced", url="https://revanced.net/")],
        [InlineKeyboardButton("🛡️ Kaspersky Antivirus Pro", url="https://m.happymod.com/kaspersky-antivirus-applock-mod/com.kms.free/")],
        [InlineKeyboardButton("📥 SnapTube (تحميل الفيديوهات)", url="https://m.happymod.com/snaptube-mod/com.snaptube.premium/")],
        [InlineKeyboardButton("🎨 Canva Pro (مميزات مدفوعة)", url="https://m.happymod.com/canva-mod/com.canva.editor/")],
        [InlineKeyboardButton("📂 ZArchiver Pro (نسخة مدفوعة)", url="https://m.happymod.com/zarchiver-donate-mod/ru.zdevs.zarchiver.pro/")],
        [InlineKeyboardButton("🎥 InShot Pro", url="https://m.happymod.com/inshot-video-editor-mod/com.camerasideas.instashot/")],
        [InlineKeyboardButton("🌀 Truecaller Gold", url="https://m.happymod.com/truecaller-caller-id-block-mod/com.truecaller/")],
        [InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

# 3. المعالجات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    welcome = f"🫡 **مرحباً بك سيادة القائد**" if user_id == OWNER_ID else "🎮 **مرحباً بك في إمبراطورية Swim-Core**"
    await update.message.reply_text(welcome + "\nاختر القسم المطلوب من الأسفل:", parse_mode='Markdown', reply_markup=main_menu_keyboard(user_id))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ **مكتبة الـ 30 لعبة (أساطير PSP):**", parse_mode='Markdown', reply_markup=games_menu_keyboard())
    elif query.data == 'apps_menu':
        await query.edit_message_text(text="📲 **ترسانة التطبيقات المهكرة (Premium):**", parse_mode='Markdown', reply_markup=apps_menu_keyboard())
    elif query.data == 'help_menu':
        await query.edit_message_text(text="📚 **دليل التشغيل:**\n1. حمل الملف.\n2. فك الضغط بـ ZArchiver Pro.\n3. استمتع باللعب!", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))
    elif query.data == 'dev':
        await query.edit_message_text(text="🎖️ **هوية المطور:**\n👤 القائد سويم (Architect)\n📡 @Swim_Architect", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))
    elif query.data == 'status' and user_id == OWNER_ID:
        await query.edit_message_text(text="📡 **حالة النظام:**\n✅ ألعاب: 30\n✅ تطبيقات: 10\n🚀 السيرفر: مستقر", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))
    elif query.data == 'back_to_main':
        await query.edit_message_text(text="القائمة الرئيسية:", reply_markup=main_menu_keyboard(user_id))

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)
