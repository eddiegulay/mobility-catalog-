"""Groq LLM initialization and configuration."""

from langchain_groq import ChatGroq
from config.settings import settings


def get_llm():
    """
    Initialize and return a configured LLM instance.
    
    Uses Anthropic Claude when MONEY_MODE is enabled (no rate limits),
    otherwise uses Groq models (free tier with rate limits).
    
    Returns:
        ChatAnthropic or ChatGroq: Configured language model instance
        
    Raises:
        ValueError: If required API keys are not set
    """
    settings.validate()
    
    if settings.MONEY_MODE:
        # Money mode: Use Anthropic Claude (premium, no rate limits)
        from langchain_anthropic import ChatAnthropic
        
        llm = ChatAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
            model=settings.CLAUDE_MODEL,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
        
        return llm
    else:
        # Free mode: Use Groq models (rate limits apply)
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
        
        return llm


# Default LLM instance for reuse across the application
llm = get_llm()
