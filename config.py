# config.py
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
PDF_FILE_PATH = os.getenv("PDF_FILE_PATH")
WEBHOOK_SECRET = os.getenv("botserver")
