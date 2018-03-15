#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from telegram.error import InvalidToken
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

from settings import DEBUG, TOKEN
import database as db

# Enable logging.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def debug(bot, update):
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    reply = "ChatID: %i\nUserID: %i" % (chat.id, user.id)

    message.reply_text(reply)


def register_update(bot, update):
    """
    This function is called for every update that contains the message field.
    Here the database is updated if the chat or sender is not registered yet.
    Private chats will be ignored by this function.
    """
    chat = update.effective_chat
    user = update.effective_user

    # Ignore private messages.
    if chat.id > 0:
        return

    # Add unknown chat members.
    if not db.chat_has_member(user, chat):
        db.add_chat_member(user, chat)


def register_text(bot, update):
    """
    A user send a text message, the bot should register the message.
    """
    register_update(bot, update)

    chat = update.effective_chat
    message = update.effective_message

    # Ignore private messages.
    if chat.id > 0:
        return

    db.add_text_message(message)


def register_user_enters(bot, update):
    """
    One or more users enter the group, the bot should register the change.
    """
    register_update(bot, update)

    chat = update.effective_chat
    message = update.effective_message
    me = bot.get_me()

    for user in message.new_chat_members:
        if user == me:
            db.set_chat_active(chat)
            continue

        if not db.chat_has_member(user, chat):
            db.add_chat_member(user, chat)
        else:
            db.set_chat_member_active(user, chat)


def register_user_leaves(bot, update):
    """
    A user left the chat, the bot should register the change.
    """
    register_update(bot, update)

    chat = update.effective_chat
    message = update.effective_message
    user = message.left_chat_member

    if user == bot.get_me():
        db.set_chat_active(chat, False)
        return

    if not db.chat_has_member(user, chat):
        db.add_chat_member(user, chat)

    db.set_chat_member_active(user, chat, False)


def quote(bot, update):
    """
    A user used the quote command.
    """
    register_update(bot, update)

    chat = update.effective_chat
    message = update.effective_message

    # Ignore private messages.
    if chat.id > 0:
        return

    # TODO Check for muted users.

    quote = db.get_random_quote(chat)

    if not quote:
        return

    message.reply_text(quote, quote=False)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the event handler and pass it your bot's token.
    try:
        updater = Updater(TOKEN)
    except InvalidToken:
        exit('Bot token is invalid.')

    bot = updater.bot

    # Get the dispatcher to register handlers.
    dp = updater.dispatcher

    # Answer the messages and commands.
    dp.add_handler(MessageHandler(Filters.text, register_text))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                  register_user_enters))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member,
                                  register_user_leaves))

    if DEBUG:
        dp.add_handler(CommandHandler("debug", debug))
    dp.add_handler(CommandHandler("quote", quote))

    dp.add_handler(MessageHandler(Filters.all, register_update))

    # Register all errors.
    dp.add_error_handler(error)

    # Start the bot.
    updater.start_polling()

    # Notify that the bot is running.
    me = bot.get_me()
    print('Your bot named %s is now running, start a conversation: '
          'https://telegram.me/%s' % (me.first_name, me.username))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
