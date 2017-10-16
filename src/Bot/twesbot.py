#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from telegram.error import InvalidToken
from telegram.ext import Updater, CommandHandler

from src.Bot.database import *

TOKEN = None
DB_CONN = None

# Enable logging.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def quote(bot, update):
    pass


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the event handler and pass it your bot's token.
    try:
        updater = Updater(TOKEN)
    except InvalidToken:
        exit('Bot token is invalid.')

    bot = updater.bot

    # Get the dispatcher to register handlers.
    dp = updater.dispatcher

    # Answer the commands and messages.
    dp.add_handler(CommandHandler('quote', quote))

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
    import os
    import sys
    import argparse
    import json
    p = argparse.ArgumentParser()
    p.add_argument('--settings', '-s',
                   help='settings file to use',
                   default='settings.json')
    args = p.parse_args(sys.argv[1:])

    try:
        with open(os.path.abspath(args.settings), 'r') as data_file:
            settings = json.load(data_file)
            TOKEN = settings['token']
            db_login = (
                    settings['db']['hostname'],
                    settings['db']['username'],
                    settings['db']['password'],
                    settings['db']['database.sql'],
                )
    except:
        exit('Settings file does not exist or is invalid format.')
    else:
        DB_CONN = setup_connection(db_login)

    main()
