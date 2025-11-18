import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class Settings:
    PROJECT_NAME: str = "WhatsApp Review Collector"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER")

    def validate(self):
        if not self.DATABASE_URL:
            logger.error("DATABASE_URL missing in .env")
        if not self.TWILIO_AUTH_TOKEN:
            logger.error("TWILIO_AUTH_TOKEN missing in .env")

settings = Settings()
settings.validate()
