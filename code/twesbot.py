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

    # Ignore private messages.
    if update.effective_chat.id > 0:
        return False, (None, None, None)

    chat = db.Chat(update.effective_chat)
    user = db.User(update.effective_user)
    chat_member = db.ChatMember(update.effective_user, update.effective_chat)

    if not chat.exists():
        chat.commit()
    if not user.exists():
        user.commit()
    if not chat_member.exists():
        chat_member.commit()

    return True, (chat, user, chat_member)


def register_message(bot, update):
    """
    A user send a text message, the bot should register the message.
    """
    success, (chat, user, chat_member) = register_update(bot, update)
    if not success:
        return

    db.Message(update.effective_message).commit()


def register_user_enters(bot, update):
    """
    One or more users enter the group, the bot should register the change.
    """
    success, (chat, user, chat_member) = register_update(bot, update)
    if not success:
        return

    me = bot.get_me()

    for new_user in update.effective_message.new_chat_members:
        if new_user == me:
            # TODO Set chat active
            continue

        chat_member = db.ChatMember(new_user, update.effective_chat)
        new_user = db.User(new_user)

        if not new_user.exists():
            new_user.commit()
        if not chat_member.exists():
            chat_member.commit()
        else:
            # TODO Set chat member active
            pass


def register_user_leaves(bot, update):
    """
    A user left the chat, the bot should register the change.
    """
    success, (chat, user, chat_member) = register_update(bot, update)
    if not success:
        return

    left_user = update.effective_message.left_chat_member

    if left_user == bot.get_me():
        # TODO Set chat inactive
        return

    chat_member = db.ChatMember(left_user, update.effective_chat,
                                is_active=False)
    left_user = db.User(left_user)

    if not left_user.exists():
        left_user.commit()
    if not chat_member.exists():
        chat_member.commit()
    else:
        # TODO Set chat member inactive
        pass


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
    dp.add_handler(MessageHandler(Filters.text, register_message))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                  register_user_enters))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member,
                                  register_user_leaves))

    if DEBUG:
        dp.add_handler(CommandHandler("debug", debug))

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
