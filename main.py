
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7972470874:AAE2NIWjI0ogXAQbGeuRXcrEF6Rtutuy4Cs"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ذاكرة مؤقتة للمستخدمين والقنوات
channels = []
participants = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎯 إنشاء سحب", callback_data='create')],
        [InlineKeyboardButton("📢 ربط قناة", callback_data='link')],
        [InlineKeyboardButton("⭐ إرسال نجوم", callback_data='stars')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 أهلاً بك في بوت روليت النجوم!", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "create":
        if not participants:
            await query.edit_message_text("❌ لا يوجد مشاركين حالياً.")
        else:
            import random
            winner = random.choice(participants)
            await query.edit_message_text(f"🏆 الفائز هو: [{winner['name']}](tg://user?id={winner['id']})", parse_mode="Markdown")
    elif query.data == "link":
        await query.edit_message_text("🔗 من فضلك حوّل رسالة من القناة هنا لربطها.")
    elif query.data == "stars":
        await query.edit_message_text("⭐ نظام النجوم قيد التفعيل. سيتم دمجه مع Telegram Stars قريبًا.")

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not any(p['id'] == user.id for p in participants):
        participants.append({'id': user.id, 'name': user.full_name})
        await update.message.reply_text("✅ تم تسجيلك في السحب.")
    else:
        await update.message.reply_text("⚠️ أنت مسجل مسبقًا.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("انضم", join))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ بوت روليت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
