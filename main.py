import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Source and destination channel mappings
CHANNEL_MAPPINGS = {
    "-1002261820786": ["-1002255696539"],  # Example source to destination
    "-1002418710282": ["-1002292610792"],  # Another source to destination
    # Add more mappings as needed
}

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def forward_video(update: Update, context):
    """Forward only video files from source to destination channels without source channel name, keeping only the caption."""
    message = update.message or update.channel_post  # Handle both message types
    
    if not message:
        logger.info("No message found in the update.")
        return
    
    logger.info(f"Received a message from chat ID: {message.chat.id}")
    
    # Check if message is from a valid source channel
    source_channel = str(message.chat.id)  # Convert to string for easy matching
    if source_channel not in CHANNEL_MAPPINGS:
        logger.info("Message is not from a valid source channel.")
        return
    
    # Check for video
    if message.video:
        logger.info("Video detected, forwarding without source channel name...")
        caption = message.caption if message.caption else ""  # Preserve the caption only
        
        # Loop through all the destination channels for this source channel
        for destination_channel in CHANNEL_MAPPINGS[source_channel]:
            await context.bot.send_video(
                chat_id=destination_channel,
                video=message.video.file_id,
                caption=caption
            )
            logger.info(f"Video forwarded to channel {destination_channel} successfully!")
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
