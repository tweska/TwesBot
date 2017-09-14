# TwesBot
A Telegram bot made with Python. This bot is implemented using the
[python-telegram-bot wrapper](https://github.com/python-telegram-bot/python-telegram-bot)!


## how to use?
1. Create a new bot or get the bot token from your existing bot by talking to
[BotFather](https://telegram.me/BotFather). If you don't know where to start, 
use [the official tutorial](https://core.telegram.org/bots#6-botfather)!

2. Install or upgrade python-telegram-bot with:
```
$ pip install python-telegram-bot --upgrade
```
Or you can install from source with:
```
$ git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive
$ cd python-telegram-bot
$ python setup.py install
```

3. Setup TwesBot by changing the bot token in `settings.json` and customizing
the actions.

4. Run your bot using: `./twesbot.py`

5. Start talking to your bot!

TIP: You can get your ID and other information about you and the chat you are in using the `/info` command. (Make sure `enable_info_command` is set to `true` in your settings file.

TIP: You can select a custom setting file with the `--settings '<filename>'` argument.
