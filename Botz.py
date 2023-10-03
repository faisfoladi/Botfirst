import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler, CallbackContext

# Set your bot token here
BOT_TOKEN = '6023368456:AAH1VbbHH7_6nW1lb2BoETdahGuhJufhU_o'

# Initialize the Updater
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Enable logging (optional)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Dictionary to track user warnings and mutes
user_warnings = {}
user_mutes = {}

# Admins who have control over the bot
admins = [5418746418]  # Replace with your admin user IDs

# Function to issue a warning and mute if necessary
def warn_and_mute(update, user_id):
    # Issue a warning
    update.message.reply_text("Your message contains forbidden content. This is your first warning.")

    # Check the number of warnings for the user
    if user_warnings.get(user_id, 0) >= 2:
        # If the user has received 3 warnings, mute them for 10 minutes (adjust as needed)
        user_mutes[user_id] = True
        update.message.reply_text("You have been muted for 10 minutes due to repeated warnings.")
        
        # Schedule unmute after 10 minutes
        job_queue = updater.job_queue
        job_queue.run_once(unmute_user, 600, context=update.message.chat_id, name=str(user_id))

    else:
        # Increment the warning count for the user
        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

# Function to unmute a user
def unmute_user(context):
    chat_id = context.job.context
    user_id = int(context.job.name)
    
    # Remove the mute for the user
    if user_mutes.get(user_id, False):
        user_mutes[user_id] = False
        context.bot.send_message(chat_id, f"User {user_id} has been unmuted.")

# Function to respond to the /start command
def start(update, context):
    user_id = update.message.from_user.id
    if user_id in admins:
        # Admin control panel with buttons
        keyboard = [[telegram.InlineKeyboardButton("Lock Bot", callback_data='lock_bot')],
                    [telegram.InlineKeyboardButton("Unlock Bot", callback_data='unlock_bot')],
                    [telegram.InlineKeyboardButton("View Warned Users", callback_data='view_warned_users')]]

        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Welcome, Admin! Use the buttons below:", reply_markup=reply_markup)
    else:
        update.message.reply_text("Welcome to the Bot! Send /info to get information about yourself.")

# Function to get user info
def user_info(update, context):
    user = update.message.from_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    info_message = f"User ID: {user_id}\nUsername: {username}\nFirst Name: {first_name}\nLast Name: {last_name}"

    update.message.reply_text(info_message)

# Function to handle text messages
def handle_text(update, context):
    user_id = update.message.from_user.id
    message_text = update.message.text.lower()  # Convert message text to lowercase for case-insensitive filtering

    # Implement message filtering for spam/forbidden content and respond accordingly
    if "spam" in message_text or "forbidden" in message_text:
        if not user_mutes.get(user_id, False):
            warn_and_mute(update, user_id)
        return

# Function to handle button clicks
def button_click(update, context):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'lock_bot':
        # Lock the bot functionality
        if user_id in admins:
            # Implement lock functionality here
            pass
    elif query.data == 'unlock_bot':
        # Unlock the bot functionality
        if user_id in admins:
            # Implement unlock functionality here
            pass
    elif query.data == 'view_warned_users':
        # View a list of warned users
        if user_id in admins:
            # Implement viewing warned users functionality here
            pass

# Add command handlers for admins and users
start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', user_info)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)

# Add message handler with Filters.text & ~Filters.command for message filtering
text_handler = MessageHandler(Filters.text & ~Filters.command, handle_text)
dispatcher.add_handler(text_handler)

# Add callback query handler for button clicks
dispatcher.add_handler(CallbackQueryHandler(button_click))

# Start the bot
updater.start_polling()

# Run the bot until you manually stop it
updater.idle()
