from chains import search_chain, reader_chain, writer_chain, critic_chain, fact_check_chain, summary_chain
import pandas as pd
import json

def run_search(topic: str) -> str:
    """Execute search agent and return raw JSON string."""
    chain = search_chain()
    result = chain.invoke({"topic": topic})
    return result

def parse_search_results(raw: str) -> pd.DataFrame:
    """Parse the JSON list from search agent into a DataFrame."""
    try:
        data = json.loads(raw)
        df = pd.DataFrame(data)
        if not df.empty:
            df["reliability_score"] = pd.to_numeric(df["reliability_score"], errors="coerce")
        return df
    except Exception:
        # Fallback: return empty DataFrame
        return pd.DataFrame()

def run_reader(sources_df: pd.DataFrame) -> str:
    """Select top sources and scrape them."""
    if sources_df.empty:
        return "No sources available."
    top_sources = sources_df.nlargest(2, "reliability_score")[["title", "url", "snippet"]].to_string(index=False)
    chain = reader_chain()
    result = chain.invoke({"sources": top_sources})
    return result

def run_writer(topic: str, search_raw: str, reader_content: str) -> str:
    """Generate full report."""
    research = f"SEARCH RESULTS:\n{search_raw}\n\nDETAILED CONTENT:\n{reader_content}"
    chain = writer_chain()
    return chain.invoke({"topic": topic, "research": research})

def run_critic(report: str) -> str:
    chain = critic_chain()
    return chain.invoke({"report": report})

def run_fact_checker(report: str, sources_raw: str) -> str:
    chain = fact_check_chain()
    return chain.invoke({"report": report, "sources": sources_raw})

def run_summarizer(report: str) -> str:
    chain = summary_chain()
    return chain.invoke({"report": report})