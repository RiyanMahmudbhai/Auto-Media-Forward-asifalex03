import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Bot token from BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Source and destination channel IDs
SOURCE_CHANNEL_ID = -1002100804603
DESTINATION_CHANNEL_ID = -1002334248978

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def forward_media(update: Update, context):
    """Forward media files from source to destination channel."""
    message = update.message

    # Check if the message is from the source channel
    if message.chat.id == SOURCE_CHANNEL_ID:
        # Forward the message to the destination channel
        await message.forward(chat_id=DESTINATION_CHANNEL_ID)

def main():
    # Initialize the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add a handler for messages containing media
    media_handler = MessageHandler(
        filters.ALL & ~filters.TEXT,
        forward_media
    )
    application.add_handler(media_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
