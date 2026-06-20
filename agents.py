from chains import search_chain, reader_chain, writer_chain, critic_chain, fact_check_chain, summary_chain
import pandas as pd
import json
from tavily import TavilyClient
import config

def run_search(topic: str) -> str:
    """Execute search agent using Tavily API for real-time results."""
    try:
        # Use Tavily API for real-time search
        tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)
        response = tavily_client.search(query=topic, search_depth="advanced", max_results=5)
        
        # Convert Tavily results to our format
        results = []
        for idx, item in enumerate(response.get("results", [])):
            results.append({
                "title": item.get("title", "No title"),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")[:300],  # Limit snippet length
                "reliability_score": str(min(10, max(1, 10 - idx)))  # Score based on rank
            })
        
        return json.dumps(results, indent=2)
    except Exception as e:
        # Fallback to LLM-based search if Tavily fails
        print(f"Tavily search failed: {e}. Using fallback LLM search.")
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