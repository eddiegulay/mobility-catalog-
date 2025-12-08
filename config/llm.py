"""Groq LLM initialization and configuration."""

from langchain_groq import ChatGroq
from config.settings import settings


def get_llm() -> ChatGroq:
    """
    Initialize and return a configured Groq LLM instance.
    
    Returns:
        ChatGroq: Configured Groq language model instance
        
    Raises:
        ValueError: If GROQ_API_KEY is not set
    """
    settings.validate()
    
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
    )
    
    return llm


# Default LLM instance for reuse across the application
llm = get_llm()
