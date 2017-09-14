import json

import telegram
import random
from telegram.ext import CommandHandler, RegexHandler

# Open the settings file.
with open('settings.json', 'r') as data_file:
    settings = json.load(data_file)

# Create the admin list, whitelist and mute list.
admins = settings['users']['admins']
whitelist = settings['users']['whitelisted'] + settings['groups']['whitelisted']
muted = settings['users']['muted'] + settings['groups']['muted']
use_whitelist = settings['bot']['use_whitelist']


# Return the bot token from the settings file.
def get_bot_token():
    return settings['bot']['token']


# Returns true if the user is allowed to interact with the bot, false otherwise.
def is_allowed_to_interact(id):
    return (not use_whitelist or id in admins + whitelist) and id not in muted


# Return true if the user is an admin, false otherwise.
def is_admin(id):
    return id in admins


# Return true if the user is whitelisted, false otherwise.
def is_whitelisted(id):
    return id in whitelist


# Return true if the user is muted, false otherwise.
def is_muted(id):
    return id in muted


def add_to_whitelist(id):
    if is_whitelisted(id):
        return

    if id < 0:
        settings['groups']['whitelisted'].append(id)
    else:
        settings['users']['whitelisted'].append(id)

    whitelist.append(id)

    with open('settings.json', 'w') as data_file:
        json.dump(settings, data_file)


# Choose a random string from the list of responses, insert the requester's name
# and send the reply.
def send_response(responses, update):
    response = random.choice(responses)
    response = response.replace("%name%", update.effective_user.first_name)
    update.message.reply_text(response, quote=False)


# Lookup the response for incoming trigger words and send it.
def generic_message_handler(bot, update):
    if not is_allowed_to_interact(update.effective_user.id):
        return

    triggers = settings['actions']['triggers']
    send_response([trigger['response'] for trigger in triggers for string in
                   trigger['regex'] if string.lower() in
                   update.message.text.lower()][0],
                  update)


# Lookup the response for incoming commands and send it.
def generic_command_handler(bot, update):
    if not is_allowed_to_interact(update.effective_user.id):
        return

    for entity in update.message.parse_entities():
        string = telegram.Message.parse_entity(update.message, entity)[1:]
        string = string.partition('@')[0]
        commands = settings['actions']['commands']
        send_response([cmd['response'] for cmd in commands
                       if string in cmd['command']][0],
                      update)
        return


# Generate the StringRegexHandlers for the triggers.
def get_trigger_handlers():
    return [RegexHandler("(?i).*" + regex, generic_message_handler) for triggers
            in settings['actions']['triggers'] for regex in triggers['regex']]


# Generate the CommandHandlers for the commands.
def get_command_handlers():
    return [CommandHandler(cmd, generic_command_handler) for cmds in
            settings['actions']['commands'] for cmd in cmds['command']]


# Combine the StringRegexHandlers and the CommandHandlers and return them.
def get_handlers():
    return get_command_handlers() + get_trigger_handlers()
