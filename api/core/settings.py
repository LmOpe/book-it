import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Settings class to hold application configuration.

    This class is used to load environment variables and set default values for
    application settings. It uses the `os` module to access environment variables
    """
    PROJECT_NAME: str = "Music Booking App"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

settings = Settings()
