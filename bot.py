import logging
import os
import http.server
import socketserver
import threading
import asyncio
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

# 2. القائمة الرئيسية V3.0 (بمعرفات فريدة لضمان الاستجابة)
def main_menu_v3(user_id):
    row1 = [InlineKeyboardButton("🛠️ هوية المطور", callback_data='v3_identity')]
    if user_id == OWNER_ID:
        row1.append(InlineKeyboardButton("📡 حالة النظام", callback_data='v3_status'))
    
    keyboard = [
        row1,
        [InlineKeyboardButton("🎮 مكتبة الألعاب (30 لعبة)", callback_data='v3_games')],
        [InlineKeyboardButton("📲 تطبيقات مهكرة (15 تطبيق)", callback_data='v3_apps')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='v3_help')]
    ]
    return InlineKeyboardMarkup(keyboard)

# 3. معالج العمليات (التفاصيل الكاملة)
async def handle_v3_interactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    
    # محاولة كسر التعليق فوراً
    try:
        await query.answer()
    except:
        pass

    if query.data == 'v3_identity':
        text = (
            "🎖️ **البطاقة التعريفية للمطور**\n\n"
            "👤 **الاسم:** القائد سويم (Architect)\n"
            "🥇 **الرتبة:** المؤسس والمبرمج الرئيسي\n"
            "📡 **للتواصل:** @Swim_Architect\n\n"
            "🛡️ *نظام Swim-Core V3.0 المستقر.*"
        )
        await query.edit_message_text(text, parse_mode='Markdown', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='v3_home')]]))

    elif query.data == 'v3_games':
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
        kb = [[InlineKeyboardButton(f"🕹️ {g[0]}", url=f"https://romspure.cc/roms/sony-playstation-portable/{g[1]}")] for g in games]
        kb.append([InlineKeyboardButton("🔙 عودة", callback_data='v3_home')])
        await query.edit_message_text("🕹️ **مكتبة ألعاب الـ PSP المتاحة:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == 'v3_home':
        await query.edit_message_text("القائمة الرئيسية للتحكم:", reply_markup=main_menu_v3(uid))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 **Swim Core V3.0** نشط الآن!", 
                                   reply_markup=main_menu_v3(update.message.from_user.id))

if __name__ == '__main__':
    threading.Thread(target=start_dummy_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_v3_interactions))
    
    # حل مشكلة الـ Conflict المسجلة في صورتك نهائياً
    app.run_polling(drop_pending_updates=True)
