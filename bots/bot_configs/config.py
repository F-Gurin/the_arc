import sys
sys.path.append('../')
sys.path.append('./')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from dotenv import load_dotenv
load_dotenv("venv/.env")
PATIENTS_BOT_TOKEN = os.environ.get("PATIENTS_BOT_TOKEN")
PSYCHOLOGISTS_BOT_TOKEN = os.environ.get("PSYCHOLOGISTS_BOT_TOKEN")
