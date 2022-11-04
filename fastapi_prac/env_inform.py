import os

FRONT_URL = os.environ.get("EXTERNAL_FRONT_URL", "http://127.0.0.1:5173")
DB_LOGIN_INFORM = os.environ.get("DB_LOGIN", "")