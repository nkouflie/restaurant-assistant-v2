import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
if not TWILIO_ACCOUNT_SID:
    raise ValueError("TWILIO_ACCOUNT_SID environment variable is not set")

TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
if not TWILIO_AUTH_TOKEN:
    raise ValueError("TWILIO_AUTH_TOKEN environment variable is not set")

TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
if not TWILIO_PHONE_NUMBER:
    raise ValueError("TWILIO_PHONE_NUMBER environment variable is not set")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
