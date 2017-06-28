#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import logging
import settings

# Enable logging.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the event handler and pass it your bot's token.
    updater = Updater(settings.get_bot_token())
    bot = updater.bot

    # Get the dispatcher to register handlers.
    dp = updater.dispatcher

    # Answer the commands and messages.
    for handler in settings.get_handlers():
        dp.add_handler(handler)

    # Register all errors.
    dp.add_error_handler(error)

    # Start the bot.
    updater.start_polling()

    # Notify that the bot is running.
    me = bot.get_me()
    print('Your bot named %s is now running, start a conversation: '
          'https://telegram.me/%s' % (me.first_name, me.username))

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM
    # or SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
