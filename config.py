import os
from dotenv import load_dotenv

load_dotenv()

# API keys with validation
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Validate API keys are present
if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    raise ValueError(
        "GROQ_API_KEY not found or not configured. "
        "Please set it in your .env file. "
        "Get your key from: https://console.groq.com/keys"
    )

if not TAVILY_API_KEY or TAVILY_API_KEY == "your_tavily_api_key_here":
    raise ValueError(
        "TAVILY_API_KEY not found or not configured. "
        "Please set it in your .env file. "
        "Get your key from: https://app.tavily.com/"
    )

# ── Free Groq models (verified as free on Groq Cloud) ──
MODEL_MAP = {
    "searcher":     "llama-3.3-70b-versatile",
    "reader":       "llama-3.3-70b-versatile",
    "writer":       "llama-3.3-70b-versatile",        # free Mixtral MoE
    "critic":       "llama-3.3-70b-versatile",        # large enough for critique
    "fact_checker": "llama-3.3-70b-versatile",
    "summarizer":   "llama-3.3-70b-versatile",
}

# Agent configuration (temperature, max_tokens)
AGENT_CONFIG = {
    "searcher":     {"temperature": 0.1, "max_tokens": 512},
    "reader":       {"temperature": 0.0, "max_tokens": 1024},
    "writer":       {"temperature": 0.7, "max_tokens": 2048},
    "critic":       {"temperature": 0.3, "max_tokens": 1024},
    "fact_checker": {"temperature": 0.0, "max_tokens": 512},
    "summarizer":   {"temperature": 0.4, "max_tokens": 512},
}