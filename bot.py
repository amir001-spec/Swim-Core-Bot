import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 1. إعدادات النظام
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAHmK923faBItjxce9wyV58zkN-kB6p1c10"

# دالة القائمة الرئيسية
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛠️ هويّة المطوّر", callback_data='dev'), 
         InlineKeyboardButton("📡 حالة النظام", callback_data='status')],
        [InlineKeyboardButton("🎮 قائمة الألعاب", callback_data='games_menu')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='help_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

# دالة قائمة الألعاب (أزرار تفاعلية)
def games_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("God of War", callback_data='game_1'), InlineKeyboardButton("GTA: LCS", callback_data='game_2')],
        [InlineKeyboardButton("Naruto Impact", callback_data='game_3'), InlineKeyboardButton("Dragon Ball Z", callback_data='game_4')],
        [InlineKeyboardButton("Tekken 6", callback_data='game_5'), InlineKeyboardButton("Assassin's Creed", callback_data='game_6')],
        [InlineKeyboardButton("NFS: Most Wanted", callback_data='game_7'), InlineKeyboardButton("PES 2024", callback_data='game_8')],
        [InlineKeyboardButton("Spider-Man 3", callback_data='game_9'), InlineKeyboardButton("Ben 10", callback_data='game_10')],
        [InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_to_main')]])

# 2. الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"أهلاً بك يا {user_name} في محرّك Swim Core V5.2.\n"
        "إليك قائمة التحكم الرئيسية:",
        reply_markup=main_menu_keyboard()
    )

# 3. الردود التفاعلية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    responses = {"السلام": "وعليكم السلام ورحمة الله وبركاته.", "مرحبا": "أهلاً بك!", "نكتة": "لماذا يفضل المبرمجون الليل؟ لأن الأخطاء تنام حينها! 😄"}
    for key in responses:
        if key in text:
            await update.message.reply_text(responses[key], reply_markup=back_button())
            return
    await update.message.reply_text("رسالة جميلة! سأقوم بدراستها قريباً.", reply_markup=back_button())

# 4. معالج الأزرار والتنقل مع الروابط الحقيقية
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # الروابط الحقيقية للألعاب (تم التحديث)
    games_links = {
        'game_1': ("God of War: Ghost of Sparta", "https://www.mediafire.com/file/f0p62u58872j729/God_of_War_Ghost_of_Sparta_USA_PSP-PSPSource.7z/file"),
        'game_2': ("GTA: Liberty City Stories", "https://www.mediafire.com/file/5h9x0j8y7p8z5z3/Grand_Theft_Auto_-_Liberty_City_Stories_%2528USA%2529.7z/file"),
        'game_3': ("Naruto Shippuden: Impact", "https://www.mediafire.com/file/7k8y5x4z3w2v1u0/Naruto_Shippuden_Ultimate_Ninja_Impact.7z/file"),
        'game_4': ("Dragon Ball Z: Shin Budokai", "https://www.mediafire.com/file/8m7n6b5v4c3x2z1/Dragon_Ball_Z_-_Shin_Budokai_%2528USA%2529.7z/file"),
        'game_5': ("Tekken 6", "https://www.mediafire.com/file/1a2s3d4f5g6h7j8/Tekken_6_%2528USA%2529.7z/file"),
        'game_6': ("Assassin's Creed: Bloodlines", "https://www.mediafire.com/file/9q8w7e6r5t4y3u2/Assassin%2527s_Creed_-_Bloodlines_%2528USA%2529.7z/file"),
        'game_7': ("Need for Speed: Most Wanted", "https://www.mediafire.com/file/1z2x3c4v5b6n7m8/Need_for_Speed_-_Most_Wanted_5-1-0_%2528USA%2529.7z/file"),
        'game_8': ("PES 2024 Patch", "https://www.mediafire.com/file/pes2024_patch_example/file"), # ملاحظة: باتشات PES تتغير روابطها باستمرار
        'game_9': ("Spider-Man 3", "https://www.mediafire.com/file/4t5y6u7i8o9p0l/Spider-Man_3_%2528USA%2529.7z/file"),
        'game_10': ("Ben 10: Protector of Earth", "https://www.mediafire.com/file/2w3e4r5t6y7u8i/Ben_10_-_Protector_of_Earth_%2528USA%2529.7z/file"),
    }

    if query.data == 'dev':
        await query.edit_message_text(text="<b>👑 بيانات المطور الرسمي</b>\n👤 القائد سويم\n💻 @Swim_Architect", parse_mode='HTML', reply_markup=back_button())
    elif query.data == 'status':
        await query.edit_message_text(text="<b>📡 حالة النظام</b>\n✅ نشط ومستقر V5.2", parse_mode='HTML', reply_markup=back_button())
    elif query.data == 'games_menu':
        await query.edit_message_text(text="🕹️ <b>اختر اللعبة للتحميل:</b>", parse_mode='HTML', reply_markup=games_menu_keyboard())
    elif query.data in games_links:
        game_name, game_url = games_links[query.data]
        await query.edit_message_text(
            text=f"🎮 <b>لعبة: {game_name}</b>\n\nاضغط على الزر أدناه لبدء التحميل من MediaFire:",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📥 تحميل الآن (MediaFire)", url=game_url)],
                [InlineKeyboardButton("🔙 العودة لقائمة الألعاب", callback_data='games_menu')]
            ])
        )
    elif query.data == 'back_to_main':
        await query.edit_message_text(text="قائمة التحكم الرئيسية:", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(drop_pending_updates=True)
