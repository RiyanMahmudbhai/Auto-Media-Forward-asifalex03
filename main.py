import os
import logging
from dotenv import load_dotenv
from telegram import Update, Request
from telegram.ext import Application, MessageHandler, filters
from telegram.error import TimedOut, NetworkError
import asyncio

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Source and destination channel mappings (mapping source channel to a list of destination channels)
CHANNEL_MAPPINGS = {
    "-1002261820786": ["-1002255696539"],  # Source: channel 1 -> Destination: channel A
    "-1002418710282": ["-1002292610792"],  # Source: channel 2 -> Destination: channel B
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

    source_channel = str(message.chat.id)  # Convert to string for easy matching

    # Check if message is from a valid source channel
    if source_channel not in CHANNEL_MAPPINGS:
        logger.warning(f"Message received from unknown source channel: {source_channel}")
        return

    # Check for video
    if message.video:
        logger.info(f"Video detected in message from {source_channel}, forwarding to destination channels.")
        caption = message.caption if message.caption else ""  # Preserve the caption only
        
        # Loop through all the destination channels for this source channel
        for destination_channel in CHANNEL_MAPPINGS[source_channel]:
            try:
                await send_video_with_retry(context, destination_channel, message.video.file_id, caption)
            except (TimedOut, NetworkError) as e:
                logger.error(f"Error sending video to {destination_channel}: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
    else:
        logger.info("No video found in the message.")

async def send_video_with_retry(context, destination_channel, video_file_id, caption, retries=3):
    """Attempt to send video with retries in case of a timeout."""
    for attempt in range(retries):
        try:
            await context.bot.send_video(
                chat_id=destination_channel,
                video=video_file_id,
                caption=caption
            )
            logger.info(f"Video successfully forwarded to channel {destination_channel}.")
            break  # Exit loop if successful
        except TimedOut:
            if attempt < retries - 1:
                logger.warning(f"Timeout occurred, retrying... (Attempt {attempt + 1}/{retries})")
                await asyncio.sleep(5)  # Wait before retrying
            else:
                logger.error(f"Failed to send video to {destination_channel} after {retries} attempts.")
        except NetworkError:
            logger.error(f"Network error while sending video to {destination_channel}.")
            break  # Do not retry on network errors
        except Exception as e:
            logger.error(f"Unexpected error while sending video: {str(e)}")
            break  # Stop retrying on unexpected errors

def main():
    """Main function to start the bot."""
    # Initialize the bot application with a request timeout
    request = Request(connect_timeout=60, read_timeout=60)  # Set timeout globally here
    application = Application.builder().token(BOT_TOKEN).request(request).build()

    # Add a handler for messages containing video files only
    video_handler = MessageHandler(filters.VIDEO, forward_video)
    application.add_handler(video_handler)

    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
