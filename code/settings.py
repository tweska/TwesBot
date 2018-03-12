# Bot token provided by BotFather
TOKEN = "#############################################"

# Database info
DB_DIALECT = "postgresql"
DB_HOSTNAME = "localhost"
DB_USERNAME = "twesbot"
DB_PASSWORD = "password"
DB_DATABASE = "twesbot"

DB_URL = "%s://%s:%s@%s/%s" % (
    DB_DIALECT,
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOSTNAME,
    DB_DATABASE
)
