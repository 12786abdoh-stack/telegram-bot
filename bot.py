import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = "8673373637:AAGqI_nhLF687p_DPpsRj4RLV_1j79poOa4"

current_process = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا بك 🤖\nارسل رابط فيديو وسأقوم بتحميله لك.\nاكتب (الغاء) لايقاف التحميل.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_process
    if current_process:
        current_process.terminate()
        current_process = None
        await update.message.reply_text("تم إلغاء التحميل ❌")
    else:
        await update.message.reply_text("لا يوجد تحميل جارٍ.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_process

    url = update.message.text

    if url.lower() == "الغاء":
        await cancel(update, context)
        return

    await update.message.reply_text("⏳ جاري التحميل...")

    filename = "video.mp4"

    try:
        current_process = subprocess.Popen(
            ["yt-dlp", "-o", filename, url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        current_process.wait()

        await update.message.reply_document(document=open(filename, "rb"))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text("حدث خطأ أثناء التحميل.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("البوت يعمل...")

app.run_polling()
