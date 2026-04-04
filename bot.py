import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعدادات النظام
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛠️ هويّة المطوّر", callback_data='dev'), 
         InlineKeyboardButton("📡 حالة النظام", callback_data='status')],
        [InlineKeyboardButton("🎮 مكتبة ألعاب PSP المضمونة", callback_data='games_menu')],
        [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu_keyboard():
    # روابط مباشرة من موقع Vimm's Lair (الأكثر ضماناً في العالم)
    keyboard = [
        [InlineKeyboardButton("God of War: Ghost of Sparta", url="https://vimm.net/vault/23541")],
        [InlineKeyboardButton("GTA: Liberty City Stories", url="https://vimm.net/vault/23588")],
        [InlineKeyboardButton("Naruto: Ultimate Ninja Impact", url="https://vimm.net/vault/23974")],
        [InlineKeyboardButton("Dragon Ball Z: Shin Budokai", url="https://vimm.net/vault/23405")],
        [InlineKeyboardButton("Tekken 6", url="https://vimm.net/vault/24250")],
        [InlineKeyboardButton("Assassin's Creed: Bloodlines", url="https://vimm.net/vault/23243")],
        [InlineKeyboardButton("🔍 تصفح آلاف الألعاب الأخرى", url="https://vimm.net/vault/PSP")],
        [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 تم تحديث نظام Swim Core إلى V5.4\n"
        "تم استخدام سيرفرات Vimm المضمونة لتجنب أخطاء الشبكة.",
        reply_markup=main_menu_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'dev':
        await query.edit_message_text(text="👤 المطور: القائد سويم\n💻 @Swim_Architect", reply_markup=main_menu_keyboard())
    elif query.data == 'status':
        await query.edit_message_text(text="✅ النظام: متصل (V5.4)\n✅ السيرفر الحالي: Vimm's Lair", reply_markup=main_menu_keyboard())
    elif query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ اختر اللعبة (سيرفرات Vimm فائقة الاستقرار):", reply_markup=games_menu_keyboard())
    elif query.data == 'back_to_main':
        await query.edit_message_text(text="قائمة التحكم الرئيسية:", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)
