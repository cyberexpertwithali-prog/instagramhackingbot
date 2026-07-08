import os
import logging
from flask import Flask
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.constants import ChatMemberStatus
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
GROUP_LINK = os.getenv("GROUP_LINK")
YOUTUBE_LINK = os.getenv("YOUTUBE_LINK")
TIKTOK1 = os.getenv("TIKTOK1")
TIKTOK2 = os.getenv("TIKTOK2")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = Flask(__name__)

@app.route("/")
def home():
    return "Instagram Security Bot is Running!"


async def is_user_joined(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        ]
    except Exception:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
        [InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("▶️ YouTube", url=YOUTUBE_LINK)],
        [InlineKeyboardButton("🎵 TikTok 1", url=TIKTOK1)],
        [InlineKeyboardButton("🎵 TikTok 2", url=TIKTOK2)],
        [InlineKeyboardButton("✅ Continue", callback_data="check")],
    ]

    await update.message.reply_text(
        "Click the buttons below to continue.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Module 1", callback_data="module1")],
        [InlineKeyboardButton("Module 2", callback_data="module2")],
        [InlineKeyboardButton("Module 3", callback_data="module3")],
        [InlineKeyboardButton("Module 4", callback_data="module4")],
        [InlineKeyboardButton("Module 5", callback_data="module5")],
    ]

    await query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    joined = await is_user_joined(
        context.bot,
        query.from_user.id,
    )

    if not joined:

        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")],
            [InlineKeyboardButton("✅ Continue", callback_data="check")]
        ]

        await query.message.edit_text(
            "❌ It looks like you don't follow the required channel.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await menu(update, context)
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "module1":
        pass

    elif data == "module2":
        pass

    elif data == "module3":
        pass

    elif data == "module4":
        pass

    elif data == "module5":
        pass
      def main():

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(check_join, pattern="^check$")
    )

    application.add_handler(
        CallbackQueryHandler(buttons)
    )

    print("Bot Started Successfully...")

    application.run_polling()


if __name__ == "__main__":
    main()
