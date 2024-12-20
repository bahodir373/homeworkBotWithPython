import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging

TEACHER_ID = 783080948
TOKEN = '7874985110:AAG5OckprK9P2sz9QgIhP9fQ-cIDXDXtUkM'

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename="logs/bot.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    if user_id == TEACHER_ID:
        await update.message.reply_text(f"Assalomu alaykum, {user_name} ustoz! Xush kelibsiz.")
    else:
        await update.message.reply_text(
            f"Salom, {user_name}! Bu bot orqali o'qituvchingizga vazifalar va fayllar yuborishingiz mumkin. Vazifangiz yoki faylingizni yuboring."
        )


async def task_handler(update: Update, context):
    student = update.message.from_user

    caption = update.message.caption if update.message.caption else ''

    if update.message.text:
        task = update.message.text
        await context.bot.send_message(
            chat_id=TEACHER_ID,
            text=f"{student.first_name}dan yangi xabar: \n\n{task}"
        )
        await update.message.reply_text("Xabaringiz o'qituvchingizga yuborildi!")

    elif update.message.document:
        document = update.message.document
        await context.bot.send_document(
            chat_id=TEACHER_ID,
            document=document.file_id,
            caption=f"{student.first_name}dan yangi hujjat\n{caption}"
        )
        await update.message.reply_text("Faylingiz o'qituvchingizga yuborildi!")

    elif update.message.photo:

        photo = update.message.photo[-1] 
        await context.bot.send_photo(
            chat_id=TEACHER_ID,
            photo=photo.file_id,
            caption=f"{student.first_name}dan yangi rasm\n{caption}"
        )
        await update.message.reply_text("Rasmingiz o'qituvchingizga yuborildi!")

    elif update.message.video:
        video = update.message.video
        await context.bot.send_video(
            chat_id=TEACHER_ID,
            video=video.file_id,
            caption=f"{student.first_name}dan yangi video\n{caption}"
        )
        await update.message.reply_text("Videongiz o'qituvchingizga yuborildi!")

    else:
        await update.message.reply_text("Yuborgan narsangizni tushunolmadim. Iltimos, matn yoki fayl yuboring.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

 
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, task_handler))

    logger.info("Bot ishga tushirildi.")
    application.run_polling()
