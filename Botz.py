import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

# Setzen Sie hier Ihren Telegram-Bot-Token ein
bot_token = '6023368456:AAHGUL4ZTfGAG7MK1CqF_0pCTryQaQMjmlU'

# Initialisieren Sie den Updater mit Ihrem Bot-Token
updater = Updater(token=bot_token, use_context=True)

# Willkommensnachricht, die an neue Mitglieder gesendet wird
welcome_message = "Herzlich willkommen in unserer Gruppe!"

# Funktion, um neue Mitglieder zu begrüßen
def welcome_new_member(update, context):
    message = update.message
    new_members = message.new_chat_members
    
    for member in new_members:
        user_id = member.id
        context.bot.send_message(chat_id=message.chat_id, text=welcome_message, reply_to_message_id=message.message_id)

# Handler für neue Mitglieder
new_member_handler = MessageHandler(Filters.status_update.new_chat_members, welcome_new_member)
updater.dispatcher.add_handler(new_member_handler)

# Starten Sie den Bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot ist gestartet!")

start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(start_handler)

# Starten Sie den Bot
updater.start_polling()
updater.idle()
