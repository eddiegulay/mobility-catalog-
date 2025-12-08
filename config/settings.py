"""Global configuration settings for the LangGraph research agent project."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Groq API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    PEXELS_API_KEY: str = os.getenv("PEXELS_API_KEY", "")
    
    # LLM Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")
    FALLBACK_MODEL: str = os.getenv("FALLBACK_MODEL", "llama-3.3-70b-versatile")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))
    
    # Rate Limiting Configuration
    # Delays are in seconds, help prevent hitting API rate limits
    # With 19 parallel agents, need enough spread to stay under TPM limits
    REQUEST_DELAY_MIN: float = float(os.getenv("REQUEST_DELAY_MIN", "1.0"))
    REQUEST_DELAY_MAX: float = float(os.getenv("REQUEST_DELAY_MAX", "3.0"))
    ENABLE_RATE_LIMITING: bool = os.getenv("ENABLE_RATE_LIMITING", "true").lower() == "true"
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    def validate(self) -> None:
        """Validate that required settings are present."""
        if not self.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is required. Please set it in your .env file.\n"
                "Get your API key from: https://console.groq.com/keys"
            )
        if not self.PEXELS_API_KEY:
            raise ValueError(
                "PEXELS_API_KEY is required. Please set it in your .env file.\n"
                "Get your API key from: https://www.pexels.com/api/new/"
            )
    
    def __repr__(self) -> str:
        """String representation of settings (hiding sensitive data)."""
        return (
            f"Settings(MODEL_NAME={self.MODEL_NAME}, "
            f"TEMPERATURE={self.TEMPERATURE}, "
            f"MAX_TOKENS={self.MAX_TOKENS}, "
            f"DEBUG={self.DEBUG})"
        )


# Singleton instance
settings = Settings()
