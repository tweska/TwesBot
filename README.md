# TwesBot
A Telegram bot made with Python. This bot is implemented using the
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)!


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

3. Install or upgrade SQLAlchemy with:
```
$ pip install SQLAlchemy --upgrade
```

4. Change the token and database info in `settings.py`.

5. Setup the database using:
```
$ python
>>> import database as db
>>> db.Base.metadata.create_all(db.engine)
```

6. Run your bot using: `./twesbot.py`

7. Start talking to your bot!
