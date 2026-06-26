import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

users = {}

def menu():
    return ReplyKeyboardMarkup([
        ["🏋️ Antrenman", "🍗 Beslenme"],
        ["💧 Su", "⚖️ Kilo"],
        ["📊 Durum"]
    ], resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users[user_id] = {"water": 0, "weight": 0}

    await update.message.reply_text(
        "💪 FIT KING'e hoş geldin!\nHedefine birlikte ulaşacağız.",
        reply_markup=menu()
    )


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if user_id not in users:
        users[user_id] = {"water": 0, "weight": 0}

    if text == "💧 Su":
        users[user_id]["water"] += 500
        await update.message.reply_text("💧 500ml su eklendi!")

    elif text == "⚖️ Kilo":
        await update.message.reply_text("Kilonu yaz (örnek: 82.5)")

    elif text.replace(".", "", 1).isdigit():
        users[user_id]["weight"] = float(text)
        await update.message.reply_text(f"⚖️ Kilo kaydedildi: {text}")

    elif text == "📊 Durum":
        u = users[user_id]
        await update.message.reply_text(
            f"💧 Su: {u['water']} ml\n⚖️ Kilo: {u['weight']} kg"
        )

    elif text == "🏋️ Antrenman":
        await update.message.reply_text("Bugün: Göğüs + Triceps 💪")

    elif text == "🍗 Beslenme":
        await update.message.reply_text("Ne yedin? Yaz: örn 3 yumurta + tavuk")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

app.run_polling()
