"""Groq LLM initialization and configuration."""

from langchain_groq import ChatGroq
from config.settings import settings


def get_groq_llm():
    """Get Groq LLM instance."""
    if not settings.GROQ_API_KEY:
        return None
        
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
    )

def get_anthropic_llm():
    """Get Anthropic LLM instance."""
    if not settings.ANTHROPIC_API_KEY:
        return None
        
    from langchain_anthropic import ChatAnthropic
    return ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model=settings.CLAUDE_MODEL,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
    )

def get_llm():
    """
    Get default LLM based on settings.
    Returns Anthropic if MONEY_MODE is True, else Groq.
    """
    if settings.MONEY_MODE and settings.ANTHROPIC_API_KEY:
        return get_anthropic_llm()
    return get_groq_llm()

# Initialize instances
groq_llm = get_groq_llm()
anthropic_llm = get_anthropic_llm()

# Default LLM (legacy support and default behavior)
llm = get_llm()
