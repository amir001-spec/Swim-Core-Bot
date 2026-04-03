import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# 1. إعدادات النظام
logging.basicConfig(level=logging.INFO)
TOKEN = "8278063413:AAFVWuLjYvwHH1-17MYmv3qYKgsJpI7jr9c"

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛠️ هويّة المطوّر", callback_data='dev'), 
         InlineKeyboardButton("📡 حالة النظام", callback_data='status')],
        [InlineKeyboardButton("📚 قائمة التعليمات", callback_data='help_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_to_main')]])

# 2. الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"أهلاً بك يا {user_name} في محرّك Swim Core V5.1.\n"
        "إليك قائمة التحكم الرئيسية:",
        reply_markup=main_menu_keyboard()
    )

# 3. الردود التفاعلية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    responses = {
        "السلام": "وعليكم السلام ورحمة الله وبركاته، أنرت نظامنا.",
        "مرحبا": "أهلاً بك! كيف يمكنني مساعدتك اليوم؟",
        "نكتة": "لماذا يفضل المبرمجون الليل؟ لأن الأخطاء تنام حينها! 😄",
        "شجعني": "استمر في طريقك، فالعظمة تبدأ بخطوة صغيرة وكود بسيط.",
        "وقت": "الوقت كالسيف، استغله في بناء مشاريع مذهلة.",
        "برمجة": "البرمجة هي فن تحويل الخيال إلى واقع ملموس.",
        "تعبت": "استرح قليلاً، فالإبداع يحتاج إلى تجديد الطاقة."
    }

    found = False
    for key in responses:
        if key in text:
            await update.message.reply_text(responses[key], reply_markup=back_button())
            found = True
            break
    
    if not found:
        await update.message.reply_text("رسالة جميلة! سأقوم بدراستها قريباً.", reply_markup=back_button())

# 4. معالج الأزرار (تصحيح خطأ التنسيق هنا)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    my_username = "Swim_Architect"

    if query.data == 'dev':
        # استخدمنا HTML هنا لتفادي خطأ الرموز في اسمك
        await query.edit_message_text(
            text=f"<b>👑 بيانات المطور الرسمي 👑</b>\n\n"
                 f"<b>👤 الاسم:</b> القائد سويم\n"
                 f"<b>🌐 المعرف:</b> @{my_username}\n"
                 f"<b>💻 الرتبة:</b> Lead Architect\n"
                 f"<b>🚀 المشروع:</b> Swim Core Engine\n\n"
                 f"<i>فخورون ببناء هذا النظام معاً.</i>",
            parse_mode='HTML',
            reply_markup=back_button()
        )
    elif query.data == 'status':
        await query.edit_message_text(
            text="<b>📡 حالة النظام الحالية</b>\n\n✅ الاتصال: نشط\n✅ الاستقرار: ممتاز",
            parse_mode='HTML',
            reply_markup=back_button()
        )
    elif query.data == 'help_menu':
        await query.edit_message_text(
            text="<b>📚 قائمة التعليمات</b>\n\nجرب إرسال: (نكتة، شجعني، وقت، برمجة، تعبت)",
            parse_mode='HTML',
            reply_markup=back_button()
        )
    elif query.data == 'back_to_main':
        await query.edit_message_text(text="قائمة التحكم الرئيسية:", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("--- SYSTEM V5.1 IS READY ---")
    app.run_polling(drop_pending_updates=True)
