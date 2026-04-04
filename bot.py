import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 1. إعدادات النظام
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛠️ هويّة المطوّر", callback_data='dev'), 
         InlineKeyboardButton("📡 حالة النظام", callback_data='status')],
        [InlineKeyboardButton("🎮 مكتبة ألعاب PPSSPP", callback_data='games_menu')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='help_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # روابط لأشهر الألعاب من موقع مضمون وشغال دائماً
    keyboard = [
        [InlineKeyboardButton("God of War", url="https://www.emulatorgames.net/roms/psp/god-of-war-ghost-of-sparta/"), 
         InlineKeyboardButton("GTA: LCS", url="https://www.emulatorgames.net/roms/psp/grand-theft-auto-liberty-city-stories/")],
        
        [InlineKeyboardButton("Naruto Impact", url="https://www.emulatorgames.net/roms/psp/naruto-shippuden-ultimate-ninja-impact/"), 
         InlineKeyboardButton("Dragon Ball Z", url="https://www.emulatorgames.net/roms/psp/dragon-ball-z-shin-budokai/")],
        
        [InlineKeyboardButton("Tekken 6", url="https://www.emulatorgames.net/roms/psp/tekken-6/"), 
         InlineKeyboardButton("Assassin's Creed", url="https://www.emulatorgames.net/roms/psp/assassins-creed-bloodlines/")],
        
        [InlineKeyboardButton("PES / FIFA", url="https://www.emulatorgames.net/roms/psp/pro-evolution-soccer-2014/"), 
         InlineKeyboardButton("Ben 10", url="https://www.emulatorgames.net/roms/psp/ben-10-protector-of-earth/")],
        
        [InlineKeyboardButton("🔍 تصفح جميع الألعاب", url="https://www.emulatorgames.net/roms/psp/")],
        [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_to_main')]])

# 2. الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"أهلاً بك يا {user_name} في محرّك Swim Core V5.3.\n"
        "إليك مكتبة الألعاب المضمونة:",
        reply_markup=main_menu_keyboard()
    )

# 3. معالج الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'dev':
        await query.edit_message_text(text="<b>👑 بيانات المطور الرسمي</b>\n👤 القائد سويم\n💻 @Swim_Architect", parse_mode='HTML', reply_markup=back_button())
    elif query.data == 'status':
        await query.edit_message_text(text="<b>📡 حالة النظام</b>\n✅ نشط ومستقر V5.3\n✅ الروابط: محدثة ومضمونة", parse_mode='HTML', reply_markup=back_button())
    elif query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ <b>مكتبة ألعاب PPSSPP الموثوقة:</b>\nاختر اللعبة وسيتم نقلك لصفحة التحميل المباشرة:", parse_mode='HTML', reply_markup=games_menu_keyboard())
    elif query.data == 'back_to_main':
        await query.edit_message_text(text="قائمة التحكم الرئيسية:", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)
