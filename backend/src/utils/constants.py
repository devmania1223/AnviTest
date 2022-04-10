import re

SCHEMA_FILE = 'schema.sql'
DB_FILE = 'simple.db'
COOKIE_NAME = 'SuperSecretToken'
SECRET_KEY = 'secret'
TOKEN_VALID_IN_SECONDS = 3000
MINIMUM_PASSWORD_LENGTH = 6
EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
