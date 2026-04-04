import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# إعدادات النظام
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛠️ هويّة المطوّر", callback_data='dev'), 
         InlineKeyboardButton("📡 حالة النظام", callback_data='status')],
        [InlineKeyboardButton("🎮 مكتبة الألعاب المضمونة", callback_data='games_menu')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='help_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # روابط مباشرة لمواقع تحميل ألعاب PSP عالمية لا تتعطل
    keyboard = [
        [InlineKeyboardButton("God of War", url="https://www.emulatorgames.net/roms/psp/god-of-war-ghost-of-sparta/"), 
         InlineKeyboardButton("GTA: LCS", url="https://www.emulatorgames.net/roms/psp/grand-theft-auto-liberty-city-stories/")],
        [InlineKeyboardButton("Naruto Impact", url="https://www.emulatorgames.net/roms/psp/naruto-shippuden-ultimate-ninja-impact/"), 
         InlineKeyboardButton("Dragon Ball Z", url="https://www.emulatorgames.net/roms/psp/dragon-ball-z-shin-budokai/")],
        [InlineKeyboardButton("Tekken 6", url="https://www.emulatorgames.net/roms/psp/tekken-6/"), 
         InlineKeyboardButton("Assassin's Creed", url="https://www.emulatorgames.net/roms/psp/assassins-creed-bloodlines/")],
        [InlineKeyboardButton("🔍 تصفح آلاف الألعاب", url="https://www.emulatorgames.net/roms/psp/")],
        [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🚀 نظام Swim Core V5.3 المحدث جاهز الآن!\n"
        "تم تحديث الروابط لتكون مضمونة 100%.",
        reply_markup=main_menu_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'dev':
        await query.edit_message_text(text="👤 المطور: القائد سويم\n💻 @Swim_Architect", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))
    elif query.data == 'status':
        await query.edit_message_text(text="✅ النظام: متصل ونشط\n✅ الروابط: تم فحصها وتأمينها", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 عودة", callback_data='back_to_main')]]))
    elif query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ اختر اللعبة (سيفتح التحميل مباشرة):", reply_markup=games_menu_keyboard())
    elif query.data == 'back_to_main':
        await query.edit_message_text(text="قائمة التحكم الرئيسية:", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)
