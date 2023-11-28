import os
from urllib import parse

import databases

DB_NAME = os.environ["BACKEND_DB_NAME"]
DB_USER = os.environ["BACKEND_DB_USER"]
DB_PASSWORD = parse.quote_plus(os.environ["BACKEND_DB_PASSWORD"])
DB_HOST = os.environ["BACKEND_DB_HOST"]
DB_PORT = os.environ["BACKEND_DB_PORT"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = databases.Database(DATABASE_URL)
