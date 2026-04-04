import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. إعدادات النخبة (التوكن والـ ID الخاص بك)
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"
OWNER_ID = 8078183906 

def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# 2. هندسة القوائم (تم إدراج الـ 30 لعبة والـ 15 تطبيقاً يدوياً)
def main_menu_keyboard(user_id):
    # زر الهوية وحالة النظام (للمالك فقط) في الصف الأول
    top_row = [InlineKeyboardButton("🛠️ هوية المطور", callback_data='dev_info')]
    if user_id == OWNER_ID:
        top_row.append(InlineKeyboardButton("📡 حالة النظام", callback_data='sys_status'))
    
    keyboard = [
        top_row,
        [InlineKeyboardButton("🎮 مكتبة الألعاب المضمونة (30 لعبة)", callback_data='games_list')],
        [InlineKeyboardButton("📲 تطبيقات مهكرة (15 تطبيق)", callback_data='apps_list')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='help_list')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # قائمة الـ 30 لعبة PSP كاملة بروابطها الأصلية
    games = [
        ("God of War: Ghost of Sparta", "god-of-war-ghost-of-sparta"),
        ("GTA: Vice City Stories", "grand-theft-auto-vice-city-stories"),
        ("Naruto Shippuden: Impact", "naruto-shippuden-ultimate-ninja-impact"),
        ("Tekken 6", "tekken-6"),
        ("Dragon Ball Z: Shin Budokai", "dragon-ball-z-shin-budokai"),
        ("PES 2014", "pro-evolution-soccer-2014"),
        ("Assassin's Creed", "assassins-creed-bloodlines"),
        ("Need for Speed", "need-for-speed-most-wanted-5-1-0"),
        ("Call of Duty", "call-of-duty-roads-to-victory"),
        ("Ben 10: Protector of Earth", "ben-10-protector-of-earth"),
        ("Spider-Man 3", "spider-man-3"),
        ("FIFA 14", "fifa-14-legacy-edition"),
        ("Mortal Kombat", "mortal-kombat-unchained"),
        ("WWE SmackDown 2011", "wwe-smackdown-vs-raw-2011"),
        ("Resident Evil", "resident-evil-directors-cut"),
        ("Crash Racing", "crash-tag-team-racing"),
        ("Metal Gear Solid", "metal-gear-solid-peace-walker"),
        ("Toy Story 3", "toy-story-3"),
        ("Iron Man 2", "iron-man-2"),
        ("Sonic Rivals", "sonic-rivals"),
        ("Prince of Persia", "prince-of-persia-rival-swords"),
        ("Midnight Club 3", "midnight-club-3-dub-edition"),
        ("Dragon Ball Z: Tenkaichi", "dragon-ball-z-tenkaichi-tag-team"),
        ("Manhunt 2", "manhunt-2"),
        ("Ghost Rider", "ghost-rider"),
        ("Resistance", "resistance-retribution"),
        ("Silent Hill", "silent-hill-origins"),
        ("Dante's Inferno", "dantes-inferno"),
        ("Burnout Legends", "burnout-legends"),
        ("LEGO Batman", "lego-batman-the-videogame")
    ]
    keyboard = [[InlineKeyboardButton(f"{i+1}. {g[0]}", url=f"https://romspure.cc/roms/sony-playstation-portable/{g[1]}")] for i, g in enumerate(games)]
    keyboard.append([InlineKeyboardButton("🔙 عودة", callback_data='back_home')])
    return InlineKeyboardMarkup(keyboard)

def apps_menu_keyboard():
    # الـ 15 تطبيقاً بروابط مصلحة تعمل 100%
    apps = [
        ("Spotify Premium", "spotify-music"), ("PicsArt Gold", "picsart-ai-photo-video-editor"),
        ("CapCut Pro", "capcut"), ("YouTube ReVanced", "youtube-vanced"),
        ("Kaspersky Pro", "kaspersky-antivirus"), ("SnapTube VIP", "snaptube"),
        ("Canva Pro", "canva"), ("ZArchiver Pro", "zarchiver"),
        ("InShot Pro", "inshot"), ("Truecaller Gold", "truecaller"),
        ("Netflix Premium", "netflix"), ("TikTok Mod", "tiktok"),
        ("Minecraft PE", "minecraft"), ("CCleaner Pro", "ccleaner"),
        ("ExpressVPN", "expressvpn")
    ]
    keyboard = [[InlineKeyboardButton(name, url=f"https://liteapks.com/{slug}.html")] for name, slug in apps]
    keyboard.append([InlineKeyboardButton("🔙 عودة", callback_data='back_home')])
    return InlineKeyboardMarkup(keyboard)

# 3. معالج الأحداث (إصلاح زر الهوية والعودة)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    # قسم الهوية - مصلح ومؤكد 100%
    if query.data == 'dev_info':
        dev_text = (
            "🎖️ **بطاقة هوية المطور الرسمي**\n\n"
            "👤 **الاسم:** القائد سويم (Architect)\n"
            "🥇 **الرتبة:** مؤسس ومطور نظام Swim Core\n"
            "📡 **التواصل:** @Swim_Architect\n\n"
            "🛡️ *هوية موثقة من نظام Swim-Core 2026.*"
        )
        await query.edit_message_text(text=dev_text, parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    elif query.data == 'games_list':
        await query.edit_message_text(text="🕹️ **مكتبة الـ 30 لعبة (PSP):**", parse_mode='Markdown', reply_markup=games_menu_keyboard())

    elif query.data == 'apps_list':
        await query.edit_message_text(text="📲 **ترسانة التطبيقات (15 تطبيق):**", parse_mode='Markdown', reply_markup=apps_menu_keyboard())

    elif query.data == 'help_list':
        help_msg = (
            "📚 **دليل الاستخدام:**\n\n"
            "1️⃣ **الألعاب:** حمل الملف، فك الضغط بـ **ZArchiver**، وشغل بـ **PPSSPP**.\n"
            "2️⃣ **التطبيقات:** حمل الـ APK وثبته مباشرة."
        )
        await query.edit_message_text(text=help_msg, parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    elif query.data == 'sys_status' and uid == OWNER_ID:
        await query.edit_message_text(text="📡 **حالة النظام:** ✅ مستقر 100%\nالألعاب: 30\nالتطبيقات: 15", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    elif query.data == 'back_home':
        await query.edit_message_text(text="القائمة الرئيسية للتحكم:", reply_markup=main_menu_keyboard(uid))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 نظام Swim Core المصلح والنهائي جاهز!", 
        reply_markup=main_menu_keyboard(update.message.from_user.id))

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)
