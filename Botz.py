import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# تنظیم توکن بات خود اینجا
bot_token = '6023368456:AAHGUL4ZTfGAG7MK1CqF_0pCTryQaQMjmlU'

# تنظیم متغیر برای ذخیره وضعیت سکوت کاربران
silent_users = set()

# مقداردهی ربات با توکن
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# تنظیمات لاگینگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تابع برای خوش آمد گویی به کاربر جدید
def welcome(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    context.bot.send_message(chat_id=update.message.chat_id, text=f"سلام {user.first_name}! خوش آمدید به گروه.")

# تابع برای جواب سلام دادن
def say_hello(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    context.bot.send_message(chat_id=update.message.chat_id, text=f"سلام {user.first_name}!")

# تابع برای اخراج کردن کاربر
def kick_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == ADMIN_USER_ID:  # تغییر ADMIN_USER_ID به شناسه شما
        user_id = context.args[0] if context.args else None
        if user_id:
            context.bot.kick_chat_member(chat_id=update.message.chat_id, user_id=user_id)
            context.bot.send_message(chat_id=update.message.chat_id, text=f"کاربر {user_id} از گروه اخراج شد.")

# تابع برای سکوت کاربر
def mute_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == ADMIN_USER_ID:  # تغییر ADMIN_USER_ID به شناسه شما
        user_id = context.args[0] if context.args else None
        if user_id:
            context.bot.restrict_chat_member(chat_id=update.message.chat_id, user_id=user_id, can_send_messages=False)
            silent_users.add(user_id)
            context.bot.send_message(chat_id=update.message.chat_id, text=f"کاربر {user_id} به حالت بی صدا درآمد.")

# تابع برای آزاد کردن کاربر از اخراج و سکوت
def unban_unmute_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == ADMIN_USER_ID:  # تغییر ADMIN_USER_ID به شناسه شما
        user_id = context.args[0] if context.args else None
        if user_id:
            context.bot.unban_chat_member(chat_id=update.message.chat_id, user_id=user_id)
            if user_id in silent_users:
                context.bot.restrict_chat_member(chat_id=update.message.chat_id, user_id=user_id, can_send_messages=True)
                silent_users.remove(user_id)
            context.bot.send_message(chat_id=update.message.chat_id, text=f"کاربر {user_id} از اخراج و حالت بی صدا خارج شد.")

# تابع برای پیام‌های بدون دستور
def handle_messages(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in silent_users:
        context.bot.send_message(chat_id=update.message.chat_id, text="شما به حالت بی صدا هستید.")

# تعریف دستورات
welcome_handler = MessageHandler(Filters.status_update.new_chat_members, welcome)
hello_handler = CommandHandler('سلام', say_hello)
kick_handler = CommandHandler('بمور', kick_user, pass_args=True)
mute_handler = CommandHandler('چوپ', mute_user, pass_args=True)
unban_unmute_handler = CommandHandler('آزاد', unban_unmute_user, pass_args=True)
messages_handler = MessageHandler(Filters.text & ~Filters.command, handle_messages)

# افزودن دستورات به دیسپچر
dispatcher.add_handler(welcome_handler)
dispatcher.add_handler(hello_handler)
dispatcher.add_handler(kick_handler)
dispatcher.add_handler(mute_handler)
dispatcher.add_handler(unban_unmute_handler)
dispatcher.add_handler(messages_handler)

# شروع ربات
updater.start_polling()
updater.idle()

