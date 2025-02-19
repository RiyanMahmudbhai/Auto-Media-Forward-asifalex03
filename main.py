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
logger = logging.getLogger(__name__)

async def forward_video(update: Update, context):
    """Forward only video files from source to destination channel."""
    message = update.message
    
    if message:
        logger.info(f"Received a message from chat ID: {message.chat.id}")
    
    # Ensure message exists and contains a video before processing
    if message and message.chat and message.video:
        if message.chat.id == SOURCE_CHANNEL_ID:
            logger.info("Video detected, forwarding...")
            await message.forward(chat_id=DESTINATION_CHANNEL_ID)
            logger.info("Video forwarded successfully!")
        else:
            logger.info("Message is not from the source channel.")
    else:
        logger.info("No video found in the message.")


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
