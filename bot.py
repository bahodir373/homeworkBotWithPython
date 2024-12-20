import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging

TEACHER_ID = 5419247338
TOKEN = ''

# logs papkasini avtomatik yaratish
if not os.path.exists('logs'):
    os.makedirs('logs')

# Log fayllarini sozlash
logging.basicConfig(
    filename="logs/bot.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start komandasi uchun handler
async def start(update: Update, context):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    if user_id == TEACHER_ID:
        await update.message.reply_text(f"Assalomu alaykum, {user_name} ustoz! Xush kelibsiz.")
    else:
        await update.message.reply_text(
            f"Salom, {user_name}!👋\n\nBu bot orqali ustozga uyga vazifalaringizni yuborishingiz mumkin."
        )

# O'qituvchiga fayl va matnli vazifalarni jo'natish
async def task_handler(update: Update, context):
    student = update.message.from_user

    caption = update.message.caption if update.message.caption else ''  # Faylga ilova qilingan caption (agar mavjud bo'lsa)

    if update.message.text:
        # Matnli xabarni o'qituvchiga jo'natish
        task = update.message.text
        await context.bot.send_message(
            chat_id=TEACHER_ID,
            text=f"{student.first_name}dan yangi xabar: \n\n{task}"
        )
        await update.message.reply_text("Xabaringiz o'qituvchingizga yuborildi!")

    elif update.message.document:
        # Yuborilgan hujjatni o'qituvchiga jo'natish
        document = update.message.document
        await context.bot.send_document(
            chat_id=TEACHER_ID,
            document=document.file_id,
            caption=f"{student.first_name}dan yangi hujjat\n{caption}"
        )
        await update.message.reply_text("Faylingiz o'qituvchingizga yuborildi!")

    elif update.message.photo:
        # Yuborilgan rasmlarni o'qituvchiga jo'natish
        photo = update.message.photo[-1]  # Eng katta o'lchamdagi rasmni olish
        await context.bot.send_photo(
            chat_id=TEACHER_ID,
            photo=photo.file_id,
            caption=f"{student.first_name}dan yangi rasm\n{caption}"
        )
        await update.message.reply_text("Rasmingiz o'qituvchingizga yuborildi!")

    elif update.message.video:
        # Yuborilgan videoni o'qituvchiga jo'natish
        video = update.message.video
        await context.bot.send_video(
            chat_id=TEACHER_ID,
            video=video.file_id,
            caption=f"{student.first_name}dan yangi video\n{caption}"
        )
        await update.message.reply_text("Videongiz o'qituvchingizga yuborildi!")

    else:
        await update.message.reply_text("Yuborgan narsangizni tushunmadim. Iltimos, matn yoki fayl yuboring.")

# Botni ishga tushirish
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # /start komandasi uchun handler
    application.add_handler(CommandHandler("start", start))

    # Fayl va matnli xabarlar uchun handler
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, task_handler))

    # Botni boshlash
    logger.info("Bot ishga tushirildi.")
    application.run_polling()