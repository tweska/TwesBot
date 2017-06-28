import json
from telegram.ext import CommandHandler, RegexHandler

# Open the settings file.
with open('settings.json') as data_file:
    settings = json.load(data_file)


def get_bot_token():
    return settings['bot']['token']


def generic_message_handler(bot, update):
    update.message.reply_text('Message received!', quote=False)


def generic_command_handler(bot, update):
    update.message.reply_text('Command received!', quote=False)


# Generate the StringRegexHandlers for the triggers.
def get_regex_handlers():
    return [RegexHandler("(?i).*" + regex, generic_message_handler) for triggers
            in settings['actions']['triggers'] for regex in triggers['regex']]


# Generate the CommandHandlers for the commands.
def get_command_handlers():
    return [CommandHandler(cmd, generic_command_handler) for cmds in
            settings['actions']['commands'] for cmd in cmds['command']]


# Combine the StringRegexHandlers and the CommandHandlers and return them.
def get_handlers():
    return get_command_handlers() + get_regex_handlers()
