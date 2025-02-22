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

# A temporary dictionary to hold the settings for the user session
user_settings = {}

async def settings(update: Update, context):
    """Start the settings conversation."""
    user = update.message.from_user

    # Check if the user is the bot owner or a sudo user (Replace with your user IDs)
    sudo_users = [123456789]  # List of authorized users (bot owner or sudo users)
    if user.id not in sudo_users:
        await update.message.reply("You are not authorized to access the settings.")
        return

    # Create the buttons for setting the source and destination channel
    keyboard = [
        [InlineKeyboardButton("Set Source Channel", callback_data='set_source')],
        [InlineKeyboardButton("Set Destination Channel", callback_data='set_destination')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply("Please choose an option:", reply_markup=reply_markup)

# Define the callback for selecting a source or destination channel
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'set_source':
        # Ask the user to choose a source channel
        await query.edit_message_text("Please choose a source channel.")
        # Implement logic here to list the channels or ask the user to provide the channel ID.
        user_settings[query.from_user.id] = {'step': 'source'}
        await query.message.reply("Send me the source channel ID you want to set.")

    elif query.data == 'set_destination':
        # Ask the user to choose a destination channel
        await query.edit_message_text("Please choose a destination channel.")
        user_settings[query.from_user.id] = {'step': 'destination'}
        await query.message.reply("Send me the destination channel ID you want to set.")

# Handle the user's reply to set the channel ID
async def set_channel(update: Update, context):
    user = update.message.from_user
    user_step = user_settings.get(user.id, {}).get('step', '')

    if user_step == 'source':
        # Save the source channel ID
        user_settings[user.id]['source_channel'] = update.message.text
        await update.message.reply(f"Source Channel set to: {update.message.text}")
        # Proceed to set destination channel
        await update.message.reply("Now, please send the destination channel ID.")
        user_settings[user.id]['step'] = 'destination'

    elif user_step == 'destination':
        # Save the destination channel ID
        user_settings[user.id]['destination_channel'] = update.message.text
        await update.message.reply(f"Destination Channel set to: {update.message.text}")
        # Confirm the setup
        await update.message.reply(f"Setup complete! Source Channel: {user_settings[user.id]['source_channel']} | Destination Channel: {user_settings[user.id]['destination_channel']}")

        # Optionally, save this in persistent storage like a file or database
        # You can update your `CHANNEL_MAPPINGS` or similar here
        del user_settings[user.id]  # Clear session after completion

# Set up conversation handler
def main():
    # Initialize the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Set up the conversation handler
    settings_conversation = ConversationHandler(
        entry_points=[CommandHandler('settings', settings)],
        states={
            SOURCE: [MessageHandler(filters.TEXT, set_channel)],
            DESTINATION: [MessageHandler(filters.TEXT, set_channel)],
        },
        fallbacks=[]
    )

    # Add the handlers to the application
    application.add_handler(settings_conversation)
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()

