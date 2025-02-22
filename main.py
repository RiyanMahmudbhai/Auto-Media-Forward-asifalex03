import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

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

# States
SOURCE, DESTINATION = range(2)

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start settings conversation."""
    user = update.effective_user

    if user.id not in [5274572622]:  # Replace with your ID
        await update.message.reply_text("❌ Unauthorized.")
        return ConversationHandler.END

    if context.user_data.get('in_conversation'):
        await update.message.reply_text("⚠️ Complete the current setup or /cancel first!")
        return ConversationHandler.END

    context.user_data['in_conversation'] = True

    keyboard = [
        [InlineKeyboardButton("Set Source", callback_data='set_source'),
         InlineKeyboardButton("Set Destination", callback_data='set_dest')]
    ]
    await update.message.reply_text(
        "⚙️ Choose action:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return SOURCE

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == 'set_source':
        await query.edit_message_text("📤 Send SOURCE channel ID (e.g., -10012345678):")
        return SOURCE
    elif query.data == 'set_dest':
        await query.edit_message_text("📥 Send DESTINATION channel ID (e.g., -10087654321):")
        return DESTINATION

async def set_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save source channel."""
    source_id = update.message.text.strip()
    
    if not source_id.startswith("-100") or not source_id[1:].isdigit():
        await update.message.reply_text("❌ Invalid source ID. Must start with -100. Try again:")
        return SOURCE  # Stay in SOURCE state
    
    context.user_data['source'] = source_id
    await update.message.reply_text(
        "✅ Source saved! Now send the DESTINATION channel ID.\n"
        "To cancel, use /cancel."
    )
    return DESTINATION  # Move to DESTINATION state

async def set_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save destination channel."""
    dest_id = update.message.text.strip()
    
    if not dest_id.startswith("-100") or not dest_id[1:].isdigit():
        await update.message.reply_text("❌ Invalid destination ID. Must start with -100. Try again:")
        return DESTINATION  # Stay in DESTINATION state
    
    # Save to persistent storage (e.g., JSON/database)
    with open("channels.json", "a") as f:
        f.write(f"{context.user_data['source']} -> {dest_id}\n")
    
    await update.message.reply_text(
        f"✅ Setup complete!\n"
        f"Source: {context.user_data['source']}\n"
        f"Destination: {dest_id}"
    )
    context.user_data.clear()  # Clear session data
    return ConversationHandler.END  # Exit conversation

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current configuration."""
    context.user_data.clear()
    await update.message.reply_text("❌ Configuration canceled.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('settings', settings)],
        states={
            SOURCE: [
                CallbackQueryHandler(handle_button),
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_source)
            ],
            DESTINATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_destination)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=False  # Block new /settings during active setup
    )
    
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.VIDEO, forward_video))
    app.run_polling()

if __name__ == "__main__":
    main()
