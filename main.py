import os import logging from dotenv import load\_dotenv from telegram import Update from telegram.ext import Application, MessageHandler, filters

# Load environment variables

load\_dotenv() BOT\_TOKEN = os.getenv("BOT\_TOKEN")

# Source and destination channel IDs

SOURCE\_CHANNEL\_ID = -1002100804603 DESTINATION\_CHANNEL\_ID = -1002334248978

# Enable logging

logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO ) logger = logging.getLogger(**name**)

async def forward\_video(update: Update, context): """Forward only video files from source to destination channel without source channel name, keeping only the caption.""" message = update.message or update.channel\_post  # Handle both message types

```
if not message:
    logger.info("No message found in the update.")
    return

logger.info(f"Received a message from chat ID: {message.chat.id}")

# Check if message is from the source channel
if message.chat.id != SOURCE_CHANNEL_ID:
    logger.info("Message is not from the source channel.")
    return

# Check for video
if message.video:
    logger.info("Video detected, forwarding without source channel name...")
    caption = message.caption if message.caption else ""  # Preserve the caption only
    await context.bot.send_video(
        chat_id=DESTINATION_CHANNEL_ID,
        video=message.video.file_id,
        caption=caption
    )
    logger.info("Video forwarded successfully!")
else:
    logger.info("No video found in the message.")
```

def main(): # Initialize the bot application application = Application.builder().token(BOT\_TOKEN).build()

```
# Add a handler for messages containing video files only
video_handler = MessageHandler(filters.VIDEO, forward_video)
application.add_handler(video_handler)

# Start the bot
application.run_polling()
```

if **name** == "**main**": main()

