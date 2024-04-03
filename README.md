# Ristocloud Python Telegram Bot

Deploy-ready Telegram bot serving content obtained from the Ristocloud API. Made using the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library. Can be setup to be fed with any canteen using the Ristocloud platform. A URL is usually available in the form of a QR code, identifying the specific canteen. Such URL can be used to setup the bot on launch:

```bash
$ python bot.py <canteen url> 
```

Prior to launch, environment variables must be provisioned by populating a `.env` with values for:

- `TELEGRAM_BOT_API_KEY`: an active API key for a Telegram Bot, obtained from [BotFather](https://t.me/BotFather)
- `PG_DATABASE`: the name of an existing PostgreSQL database to be used by the bot script
- `PG_HOST`: the hostname or address of a running PostgreSQL database instance, which shall be accessible from the node on which the bot script is run
- `PG_PORT`: the port through which the aforementioned database can be reached
- `PG_USER`: a PostgreSQL user with appropriate permissions for the chosen database
- `PG_PASSWORD`: the password of the aforementioned user

Make sure of course that all dependencies are satisfied using your package/environment manager of choice, e.g. with pip:

```bash
(venv) $ pip install -r requirements.txt
```

*Note:* this bot depends on the [companion webapp](https://github.com/dododevs/tg-ristocloud-webapp) to properly function. In case you want to tweak and host your own version of it, please modify the `bot.py` file accordingly, changing the URL of the webapp from `tg-ristocloud.web.app` to the address of your webapp. It must be served over an HTTPS connection and be accessible from the public Internet.