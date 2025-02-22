import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler


# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

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

# Constants for conversation states
SOURCE, DESTINATION = range(2)

async def settings(update: Update, context):
    """Start the settings conversation."""
    user = update.effective_user

    # Authorization check
    sudo_users = [5274572622]  # Replace with your user ID
    if user.id not in sudo_users:
        await update.message.reply_text("❌ Unauthorized access.")
        return

    # Start the conversation
    keyboard = [
        [InlineKeyboardButton("Set Source Channel", callback_data='set_source')],
        [InlineKeyboardButton("Set Destination Channel", callback_data='set_destination')],
    ]
    await update.message.reply_text(
        "⚙️ Configure channels:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SOURCE  # Transition to SOURCE state

async def button_handler(update: Update, context):
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == 'set_source':
        await query.message.reply_text("📤 Send the SOURCE channel ID (e.g., -100123456789):")
        return SOURCE
    elif query.data == 'set_destination':
        await query.message.reply_text("📥 Send the DESTINATION channel ID (e.g., -100987654321):")
        return DESTINATION

async def set_source(update: Update, context):
    """Save source channel and ask for destination."""
    source_id = update.message.text.strip()
    
    # Validate channel ID format
    if not source_id.startswith("-100") or not source_id[1:].isdigit():
        await update.message.reply_text("❌ Invalid source channel ID. Must start with -100.")
        return SOURCE  # Stay in SOURCE state
    
    context.user_data['source'] = source_id
    await update.message.reply_text("✅ Source channel set! Now send the DESTINATION channel ID:")
    return DESTINATION  # Move to DESTINATION state

async def set_destination(update: Update, context):
    """Save destination channel and confirm."""
    dest_id = update.message.text.strip()
    
    if not dest_id.startswith("-100") or not dest_id[1:].isdigit():
        await update.message.reply_text("❌ Invalid destination channel ID. Must start with -100.")
        return DESTINATION  # Stay in DESTINATION state
    
    context.user_data['destination'] = dest_id
    
    # Save to persistent storage (e.g., JSON file)
    with open("channel_mappings.json", "a") as f:
        json.dump({
            "source": context.user_data['source'],
            "destination": dest_id
        }, f)
        f.write("\n")
    
    await update.message.reply_text(
        f"✅ Configuration saved!\n"
        f"Source: {context.user_data['source']}\n"
        f"Destination: {dest_id}"
    )
    return ConversationHandler.END  # End conversation

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('settings', settings)],
        states={
            SOURCE: [
                CallbackQueryHandler(button_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_source)
            ],
            DESTINATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_destination)
            ]
        },
        fallbacks=[CommandHandler('cancel', lambda u,c: ConversationHandler.END)]
    )
    
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.VIDEO, forward_video))
    application.run_polling()


if __name__ == "__main__":
    main()

