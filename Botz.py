import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Setzen Sie hier Ihren Telegram-Bot-Token ein
bot_token = '6023368456:AAHGUL4ZTfGAG7MK1CqF_0pCTryQaQMjmlU'

# Benutzer-ID des Administrators (Ihre ID). Sie müssen Ihre eigene ID einsetzen.
admin_id = '5948436434'

# Stadien für den Konversations-Handler
START, MENU = range(2)

# Benutzerdaten speichern
user_data = {}

# Initialisieren Sie den Updater mit Ihrem Bot-Token
updater = Updater(token=bot_token, use_context=True)

# Willkommensnachricht, die an neue Mitglieder gesendet wird
welcome_message = "سلام چطوری خوشومدی به گروه خودت {mention} "

# Funktion, um neue Mitglieder zu begrüßen
def welcome_new_member(update: Update, context: CallbackContext) -> int:
    message = update.message
    new_members = message.new_chat_members

    for member in new_members:
        user_id = member.id
        context.bot.send_message(chat_id=message.chat_id, text=welcome_message, reply_to_message_id=message.message_id)

# Handler für neue Mitglieder
new_member_handler = MessageHandler(Filters.status_update.new_chat_members, welcome_new_member)
updater.dispatcher.add_handler(new_member_handler)

# Funktion, um auf den Befehl /hallo zu reagieren
def say_hello(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="سلام خوبی چه خبر؟ ")

# Handler für den Befehl /hallo hinzufügen
hello_handler = CommandHandler('سلام', say_hello)
updater.dispatcher.add_handler(hello_handler)

# Funktion, um auf den Befehl /sperr zu reagieren und den Benutzer zu sperren
def ban_user(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    # Überprüfen, ob der ausführende Benutzer ein Gruppenadministrator ist
    chat_member = context.bot.get_chat_member(chat_id, user_id)
    
    if chat_member.status == 'administrator' and str(user_id) == admin_id:
        if len(context.args) == 1:
            user_to_ban_id = context.args[0]
            context.bot.kick_chat_member(chat_id=chat_id, user_id=user_to_ban_id)
            context.bot.send_message(chat_id=chat_id, text=f"کاربر {user_to_ban_id} دفن شد.")
        else:
            context.bot.send_message(chat_id=chat_id, text="Verwendung: /sperr Benutzer_ID")
    else:
        context.bot.send_message(chat_id=chat_id, text="Sie haben keine Berechtigung, diesen Befehl auszuführen.")

# Handler für den Befehl /sperr hinzufügen
ban_handler = CommandHandler('بمیر', ban_user, pass_args=True)
updater.dispatcher.add_handler(ban_handler)

# Funktion, um den Benutzer stummzuschalten
def mute_user(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    target_user_id = context.args[0] if context.args else None

    if target_user_id:
        # Überprüfen, ob der ausführende Benutzer ein Gruppenadministrator ist
        chat_member = context.bot.get_chat_member(chat_id, user_id)
        
        if chat_member.status == 'administrator' and str(user_id) == admin_id:
            context.bot.restrict_chat_member(chat_id=chat_id, user_id=target_user_id, can_send_messages=False)
            context.bot.send_message(chat_id=chat_id, text=f"Benutzer {target_user_id} امی نفر چوپ شد.")
        else:
            context.bot.send_message(chat_id=chat_id, text="Sie haben keine Berechtigung, diesen Befehl auszuführen.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Verwendung: /stummsetzen Benutzer_ID")

# Handler für den Befehl /stummsetzen hinzufügen
mute_handler = CommandHandler('چوپ', mute_user, pass_args=True)
updater.dispatcher.add_handler(mute_handler)

# Fügen Sie hier weitere Funktionen wie /info, /beitrag, /admin hinzu...

# Starten Sie den Bot
updater.start_polling()
updater.idle()
