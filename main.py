import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Source and destination channel IDs
SOURCE_CHANNEL_ID = -1002100804603
DESTINATION_CHANNEL_ID = -1002334248978

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def forward_video(update: Update, context):
    """Forward only video files from source to destination channel."""
    message = update.message
    
    # Check if the message is from the source channel and contains a video
    if message.chat.id == SOURCE_CHANNEL_ID and message.video:
        await message.forward(chat_id=DESTINATION_CHANNEL_ID)


def main():
    # Initialize the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add a handler for messages containing video files only
    video_handler = MessageHandler(filters.VIDEO, forward_video)
    application.add_handler(video_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
