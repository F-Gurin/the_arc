import os
from dotenv import load_dotenv

load_dotenv("venv/.env")
PATIENTS_BOT_TOKEN = os.environ.get("PATIENTS_BOT_TOKEN")
PSYCHOLOGISTS_BOT_TOKEN = os.environ.get("PSYCHOLOGISTS_BOT_TOKEN")
AUTHORIZED_USERS = os.environ.get("AUTHORIZED_USERS")