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
OWNER_ID = 8078183906 

def start_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# 2. القائمة الرئيسية (V3.0)
def main_menu(user_id):
    # تم تحديث callback_data لضمان الاستجابة
    row1 = [InlineKeyboardButton("🛠️ هوية المطور", callback_data='v3_dev_info')]
    if user_id == OWNER_ID:
        row1.append(InlineKeyboardButton("📡 حالة النظام", callback_data='v3_sys_status'))
    
    keyboard = [
        row1,
        [InlineKeyboardButton("🎮 مكتبة الألعاب (30 لعبة)", callback_data='v3_games')],
        [InlineKeyboardButton("📲 تطبيقات مهكرة (15 تطبيق)", callback_data='v3_apps')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='v3_help')]
    ]
    return InlineKeyboardMarkup(keyboard)

# 3. معالج التفاعل (بدون أي اختصار)
async def handle_interactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    # --- خيار هوية المطور ---
    if query.data == 'v3_dev_info':
        dev_card = (
            "🎖️ **البطاقة التعريفية للمطور**\n\n"
            "👤 **الاسم:** القائد سويم (Architect)\n"
            "🥇 **الرتبة:** المؤسس والمبرمج الرئيسي\n"
            "📡 **للتواصل:** @Swim_Architect\n\n"
            "🛡️ *نظام Swim-Core V3.0 محمي بالكامل.*"
        )
        await query.edit_message_text(dev_card, parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='v3_home')]]))

    # --- خيار حالة النظام ---
    elif query.data == 'v3_sys_status':
        status = "📡 **تقرير النظام V3.0:**\n✅ الحالة: Online\n✅ الألعاب: 30 ملف\n✅ التطبيقات: 15 ملف"
        await query.edit_message_text(status, parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='v3_home')]]))

    # --- مكتبة الألعاب (30 لعبة كاملة بروابطها) ---
    elif query.data == 'v3_games':
        games_list = [
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
        kb = [[InlineKeyboardButton(f"🕹️ {g[0]}", url=f"https://romspure.cc/roms/sony-playstation-portable/{g[1]}")] for g in games_list]
        kb.append([InlineKeyboardButton("🔙 عودة", callback_data='v3_home')])
        await query.edit_message_text("🕹️ **مكتبة ألعاب الـ PSP المتاحة:**", reply_markup=InlineKeyboardMarkup(kb))

    # --- التطبيقات المهكرة (15 تطبيق) ---
    elif query.data == 'v3_apps':
        apps_list = [
            ("Spotify Premium", "spotify-music"), ("PicsArt Gold", "picsart-photo-studio"),
            ("CapCut Pro", "capcut-video-editor"), ("YouTube ReVanced", "youtube-revanced"),
            ("Kaspersky Pro", "kaspersky-antivirus"), ("SnapTube VIP", "snaptube"),
            ("Canva Pro", "canva"), ("ZArchiver Pro", "zarchiver-pro"),
            ("InShot Pro", "inshot"), ("Truecaller Gold", "truecaller"),
            ("Netflix Premium", "netflix"), ("TikTok Mod", "tiktok"),
            ("Minecraft PE", "minecraft"), ("CCleaner Pro", "ccleaner"), ("ExpressVPN", "expressvpn")
        ]
        kb = [[InlineKeyboardButton(f"📲 {a[0]}", url=f"https://apkmody.com/apps/{a[1]}")] for a in apps_list]
        kb.append([InlineKeyboardButton("🔙 عودة", callback_data='v3_home')])
        await query.edit_message_text("📲 **ترسانة التطبيقات المهكرة:**", reply_markup=InlineKeyboardMarkup(kb))

    # --- قائمة التعليمات ---
    elif query.data == 'v3_help':
        help_txt = "📚 **دليل V3.0:**\n1. حمل اللعبة.\n2. فك الضغط بـ ZArchiver.\n3. شغل بـ PPSSPP."
        await query.edit_message_text(help_txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='v3_home')]]))

    # --- العودة ---
    elif query.data == 'v3_home':
        await query.edit_message_text("القائمة الرئيسية للتحكم:", reply_markup=main_menu(uid))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 **Swim Core V3.0**\nالنظام المحدث والمستقر جاهز!", reply_markup=main_menu(update.message.from_user.id))

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_interactions))
    # تنظيف التحديثات القديمة (Conflict Fix)
    app.run_polling(drop_pending_updates=True)
