import os
from app.config import BaseConfig


class GroqAIConfig(BaseConfig):
    """GroqAI API configuration"""

    # general GroqAI API settings
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", 1))  # default temperature

    # model-specific settings
    GROQ_MODEL = os.getenv(
        "GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"
    )  # default model
    GROQ_TOP_P = int(os.getenv("GROQ_TOP_P", 1))
    GROQ_MAX_COMPLETION_TOKENS = int(
        os.getenv("GROQ_MAX_COMPLETION_TOKENS", 1024)
    )  # default max tokens for responses

    @staticmethod
    def validate():
        """ensures that required Groq configurations are available"""
        if not GroqAIConfig.GROQ_API_KEY:
            raise EnvironmentError("Missing GROQ_API_KEY in environment variables.")
