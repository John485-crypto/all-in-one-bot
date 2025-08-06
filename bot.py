import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN or not ADMIN_ID:
    raise Exception("❌ BOT_TOKEN or ADMIN_ID is missing. Please set them in Render Environment.")

ADMIN_ID = int(ADMIN_ID)

# Flask server to keep alive (for Render pinging)
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Telegram /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 <b>Hello and welcome!</b>\n\n"
        "🔐 <b>You’ve reached our Premium VIP Membership Bot.</b>\n\n"
        "🎥 <b>Total VIP Collection:</b> <u>10,000+ exclusive videos</u> 🔥\n\n"
        "<b>Send a message to contact admin anonymously.</b>",
        parse_mode="HTML"
    )

# Forward all user messages to you (admin)
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    if user and text:
        msg = f"📩 New message from @{user.username or 'no username'} (ID: {user.id}):\n\n{text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

# Start the bot
def main():
    Thread(target=run_flask).start()  # run Flask mini-server
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    print("✅ Bot is running...")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
