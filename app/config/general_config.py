import os
from app.config import BaseConfig


class GeneralConfig(BaseConfig):
    """
    Configuration class that manages application-wide settings & environment variables.
    """

    ENV = os.getenv("ENV", "local")
    APP_PORT = int(os.getenv("APP_PORT", "8080"))  # convert to integer
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))  # convert to integer
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    DEFAULT_CLIENT = os.getenv("DEFAULT_CLIENT", "OpenAIClient")
