from langchain_groq import ChatGroq               # ← CHANGED
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import config

def get_llm(agent_role: str) -> ChatGroq:          # ← CHANGED return type
    """Return a ChatGroq instance for the given role."""
    model_name = config.MODEL_MAP.get(agent_role, "llama-3.1-8b-instant")
    cfg = config.AGENT_CONFIG.get(agent_role, {})
    return ChatGroq(
        api_key=config.GROQ_API_KEY,               # ← CHANGED: direct API key
        model=model_name,
        temperature=cfg.get("temperature", 0.0),
        max_tokens=cfg.get("max_tokens", 512),
    )

# ── Prompt templates ───────────────────────────────────────────────────
SEARCH_PROMPT = ChatPromptTemplate.from_template("""You are a research search agent. Generate a list of 5 credible sources about the topic: {topic}
Return ONLY a valid JSON array of objects with these fields:
- "title": string (source title)
- "url": string (source URL, make it plausible)
- "snippet": string (brief description)
- "reliability_score": string (0-10, as string)

NO other text, just valid JSON.""")

READER_PROMPT = ChatPromptTemplate.from_template("""You are a content reader. Extract and summarize key information from these sources:
{sources}
Provide a detailed, structured summary of the most important points.""")

WRITER_PROMPT = ChatPromptTemplate.from_template("""You are a research report writer. Write a comprehensive, well-structured research report on: {topic}
Use this research material:
{research}
Include: Introduction, Key Findings, Analysis, and Conclusion. Use markdown formatting.""")

CRITIC_PROMPT = ChatPromptTemplate.from_template("""You are a critical reviewer. Analyze this research report and provide constructive feedback:
{report}
Identify strengths, weaknesses, and areas for improvement.""")

FACT_CHECK_PROMPT = ChatPromptTemplate.from_template("""You are a fact-checker. Verify the claims in this report using the provided sources:
Report:
{report}

Sources:
{sources}
Highlight any potential inaccuracies or unsupported claims.""")

SUMMARY_PROMPT = ChatPromptTemplate.from_template("""You are an executive summarizer. Create a concise, high-level summary of this research report:
{report}
Keep it under 300 words.""")

# ── Chains (unchanged except they now use ChatGroq) ─────────────────────
def search_chain():
    return SEARCH_PROMPT | get_llm("searcher") | StrOutputParser()

def reader_chain():
    return READER_PROMPT | get_llm("reader") | StrOutputParser()

def writer_chain():
    return WRITER_PROMPT | get_llm("writer") | StrOutputParser()

def critic_chain():
    return CRITIC_PROMPT | get_llm("critic") | StrOutputParser()

def fact_check_chain():
    return FACT_CHECK_PROMPT | get_llm("fact_checker") | StrOutputParser()

def summary_chain():
    return SUMMARY_PROMPT | get_llm("summarizer") | StrOutputParser()