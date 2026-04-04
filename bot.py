import logging
import os
import http.server
import socketserver
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. الإعدادات الأساسية
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"
OWNER_ID = 8078183906 

def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# 2. هندسة القوائم (تم تثبيت المعرفات Callback IDs يدوياً)
def main_menu_keyboard(user_id):
    # زر الهوية وحالة النظام كما في صورتك تماماً
    row1 = [InlineKeyboardButton("🛠️ هوية المطور", callback_data='target_dev')]
    if user_id == OWNER_ID:
        row1.append(InlineKeyboardButton("📡 حالة النظام", callback_data='target_sys'))
    
    keyboard = [
        row1,
        [InlineKeyboardButton("🎮 مكتبة الألعاب المضمونة (30 لعبة)", callback_data='target_games')],
        [InlineKeyboardButton("📲 تطبيقات مهكرة (15 تطبيق)", callback_data='target_apps')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='target_help')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # قائمة الـ 30 لعبة كاملة بروابط مباشرة
    games = [
        ("God of War: Ghost of Sparta", "god-of-war-ghost-of-sparta"),
        ("GTA: Vice City Stories", "grand-theft-auto-vice-city-stories"),
        ("Naruto Shippuden: Impact", "naruto-shippuden-ultimate-ninja-impact"),
        ("Tekken 6", "tekken-6"), ("PES 2014", "pro-evolution-soccer-2014"),
        ("Assassin's Creed", "assassins-creed-bloodlines"), ("Need for Speed", "need-for-speed-most-wanted-5-1-0"),
        ("Call of Duty", "call-of-duty-roads-to-victory"), ("Ben 10", "ben-10-protector-of-earth"),
        ("Spider-Man 3", "spider-man-3"), ("FIFA 14", "fifa-14-legacy-edition"),
        ("Mortal Kombat", "mortal-kombat-unchained"), ("WWE 2011", "wwe-smackdown-vs-raw-2011"),
        ("Resident Evil", "resident-evil-directors-cut"), ("Crash Racing", "crash-tag-team-racing"),
        ("Metal Gear", "metal-gear-solid-peace-walker"), ("Toy Story 3", "toy-story-3"),
        ("Iron Man 2", "iron-man-2"), ("Sonic Rivals", "sonic-rivals"),
        ("Prince of Persia", "prince-of-persia-rival-swords"), ("Midnight Club 3", "midnight-club-3-dub-edition"),
        ("Dragon Ball Z", "dragon-ball-z-tenkaichi-tag-team"), ("Manhunt 2", "manhunt-2"),
        ("Ghost Rider", "ghost-rider"), ("Resistance", "resistance-retribution"),
        ("Silent Hill", "silent-hill-origins"), ("Dante's Inferno", "dantes-inferno"),
        ("Burnout Legends", "burnout-legends"), ("LEGO Batman", "lego-batman-the-videogame"),
        ("Dragon Ball Shin Budokai", "dragon-ball-z-shin-budokai")
    ]
    keyboard = [[InlineKeyboardButton(f"{i+1}. {g[0]}", url=f"https://romspure.cc/roms/sony-playstation-portable/{g[1]}")] for i, g in enumerate(games)]
    keyboard.append([InlineKeyboardButton("🔙 عودة", callback_data='back_home')])
    return InlineKeyboardMarkup(keyboard)

def apps_menu_keyboard():
    # الـ 15 تطبيقاً مع روابط بديلة لضمان عدم ظهور خطأ الاتصال
    apps = [
        ("Spotify Premium", "spotify-music"), ("PicsArt Gold", "picsart-photo-studio"),
        ("CapCut Pro", "capcut-video-editor"), ("YouTube ReVanced", "youtube-revanced"),
        ("Kaspersky Pro", "kaspersky-antivirus"), ("SnapTube VIP", "snaptube"),
        ("Canva Pro", "canva"), ("ZArchiver Pro", "zarchiver-pro"),
        ("InShot Pro", "inshot"), ("Truecaller Gold", "truecaller"),
        ("Netflix Premium", "netflix"), ("TikTok Mod", "tiktok"),
        ("Minecraft PE", "minecraft"), ("CCleaner Pro", "ccleaner"),
        ("ExpressVPN", "expressvpn")
    ]
    keyboard = [[InlineKeyboardButton(name, url=f"https://apkmody.com/apps/{slug}")] for name, slug in apps]
    keyboard.append([InlineKeyboardButton("🔙 عودة", callback_data='back_home')])
    return InlineKeyboardMarkup(keyboard)

# 3. معالج العمليات (تم الربط بالمعرفات الجديدة لضمان الاستجابة)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == 'target_dev':
        dev_info = (
            "🎖️ **هوية المطور الرسمي**\n\n"
            "👤 **الاسم:** القائد سويم (Architect)\n"
            "🥇 **الرتبة:** مؤسس نظام Swim Core\n"
            "📡 **التواصل:** @Swim_Architect\n\n"
            "⚠️ *هذا الحساب موثق رسمياً.*"
        )
        await query.edit_message_text(text=dev_info, parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    elif query.data == 'target_games':
        await query.edit_message_text(text="🕹️ **مكتبة الألعاب (30 لعبة):**", parse_mode='Markdown', reply_markup=games_menu_keyboard())

    elif query.data == 'target_apps':
        await query.edit_message_text(text="📲 **التطبيقات المهكرة (15 تطبيق):**", parse_mode='Markdown', reply_markup=apps_menu_keyboard())

    elif query.data == 'target_help':
        msg = "📚 **تعليمات:** فك الضغط بـ ZArchiver ثم شغل بـ PPSSPP."
        await query.edit_message_text(text=msg, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_home')]]))

    elif query.data == 'back_home':
        await query.edit_message_text(text="القائمة الرئيسية:", reply_markup=main_menu_keyboard(uid))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Swim Core V8.0 نشط الآن!", reply_markup=main_menu_keyboard(update.message.from_user.id))

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # الحل السحري لمشكلة الـ Conflict المذكورة في صورتك
    app.run_polling(drop_pending_updates=True, stop_signals=None)
