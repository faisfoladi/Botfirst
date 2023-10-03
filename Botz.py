import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler

# Initialize the bot
updater = Updater(token='6023368456:AAH1VbbHH7_6nW1lb2BoETdahGuhJufhU_o', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Admin user IDs
admins = [5418746418, 456]

# User warnings and mutes
user_warnings = {}
user_mutes = {}

# Conversation states (if needed)
STATE1 = 1

# Function to send a welcome message
def send_welcome(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to the group!")

# Function to handle /start command
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in admins:
        keyboard = [[InlineKeyboardButton("Mute User", callback_data='mute_user')],
                    [InlineKeyboardButton("Unmute User", callback_data='unmute_user')],
                    [InlineKeyboardButton("View Warned Users", callback_data='view_warned_users')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Admin options:", reply_markup=reply_markup)
    else:
        send_welcome(update, context)

# Function to handle text messages
def handle_text(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    message_text = update.message.text.lower()

    # Message filtering and anti-spam logic
    if "spam" in message_text or "forbidden" in message_text:
        if not user_mutes.get(user_id, False):
            warn_and_mute(update, user_id)
        return

# Function to warn and potentially mute a user
def warn_and_mute(update: Update, user_id: int):
    update.message.reply_text("Your message contains forbidden content. This is your first warning.")
    user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

    if user_warnings.get(user_id, 0) >= 2:
        mute_user(update, user_id)

# Function to mute a user
def mute_user(update: Update, user_id: int):
    user_mutes[user_id] = True
    update.message.reply_text("You have been muted for 10 minutes due to repeated warnings.")

    # Schedule unmute after 10 minutes
    context = update.message.chat_id
    updater.job_queue.run_once(unmute_user, 600, context=context, name=str(user_id))

# Function to unmute a user
def unmute_user(context: CallbackContext):
    chat_id = context.job.context
    user_id = int(context.job.name)
    if user_mutes.get(user_id, False):
        user_mutes[user_id] = False
        context.bot.send_message(chat_id, f"User {user_id} has been unmuted.")

# Function to handle button clicks
def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'mute_user':
        mute_user(update, user_id)
    elif query.data == 'unmute_user':
        unmute_user(context, query.message.chat_id, user_id)
    elif query.data == 'view_warned_users':
        view_warned_users(update)

# Function to view warned users (admin-only)
def view_warned_users(update: Update):
    admin_id = update.callback_query.from_user.id
    if admin_id not in admins:
        return

    warned_users = [f"User {user_id}: {count} warnings" for user_id, count in user_warnings.items() if count > 0]
    if warned_users:
        update.callback_query.message.reply_text("\n".join(warned_users))
    else:
        update.callback_query.message.reply_text("No users have been warned.")

# Define conversation handler (if needed)
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={},
    fallbacks=[]
)

# Add handlers to dispatcher
dispatcher.add_handler(conversation_handler)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
dispatcher.add_handler(CallbackQueryHandler(button_click))

# Start the bot
updater.start_polling()

# Run the bot until you manually stop it
updater.idle()
