import os
from dotenv import load_dotenv

load_dotenv()

# API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

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