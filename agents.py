from chains import search_chain, reader_chain, writer_chain, critic_chain, fact_check_chain, summary_chain
import pandas as pd
import json
import logging
from tavily import TavilyClient
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MAX_SNIPPET_LENGTH = 300
MAX_RELIABILITY_SCORE = 10
MIN_RELIABILITY_SCORE = 1
MAX_TOPIC_LENGTH = 500

def validate_topic(topic: str) -> tuple[bool, str]:
    """
    Validate research topic input.
    
    Args:
        topic: User-provided research topic
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not topic or len(topic.strip()) == 0:
        return False, "Topic cannot be empty"
    if len(topic) > MAX_TOPIC_LENGTH:
        return False, f"Topic too long (max {MAX_TOPIC_LENGTH} characters)"
    return True, ""

def run_search(topic: str) -> str:
    """
    Execute search agent using Tavily API for real-time results.
    
    Args:
        topic: Research topic string (max 500 chars)
        
    Returns:
        JSON string containing list of search results
        
    Raises:
        ValueError: If topic is invalid
    """
    # Validate input
    is_valid, error_msg = validate_topic(topic)
    if not is_valid:
        raise ValueError(error_msg)
    
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
                "snippet": item.get("content", "")[:MAX_SNIPPET_LENGTH],
                "reliability_score": str(min(MAX_RELIABILITY_SCORE, max(MIN_RELIABILITY_SCORE, MAX_RELIABILITY_SCORE - idx)))
            })
        
        if not results:
            logger.warning("Tavily returned no results, using fallback")
            raise ValueError("No results from Tavily")
            
        return json.dumps(results, indent=2)
        
    except Exception as e:
        # Fallback to LLM-based search if Tavily fails
        logger.warning(f"Tavily search failed: {e}. Using fallback LLM search.")
        try:
            chain = search_chain()
            result = chain.invoke({"topic": topic})
            return result
        except Exception as fallback_error:
            logger.error(f"Fallback search also failed: {fallback_error}")
            # Return error result instead of crashing
            return json.dumps([{
                "title": "Search Error",
                "url": "",
                "snippet": f"Unable to perform search: {str(e)}",
                "reliability_score": "0"
            }])

def parse_search_results(raw: str) -> pd.DataFrame:
    """
    Parse the JSON list from search agent into a DataFrame.
    
    Args:
        raw: JSON string from run_search()
        
    Returns:
        DataFrame with columns: title, url, snippet, reliability_score
    """
    try:
        data = json.loads(raw)
        if not data:
            logger.warning("Empty data received from search results")
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        if not df.empty and "reliability_score" in df.columns:
            # Convert to numeric and fill NaN with 0
            df["reliability_score"] = pd.to_numeric(
                df["reliability_score"], 
                errors="coerce"
            ).fillna(0)
        return df
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse search results JSON: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Unexpected error parsing search results: {e}")
        return pd.DataFrame()

def run_reader(sources_df: pd.DataFrame) -> str:
    """
    Select top sources and extract detailed content.
    
    Args:
        sources_df: DataFrame with search results
        
    Returns:
        Detailed content summary from top sources
    """
    if sources_df.empty:
        logger.warning("Empty DataFrame passed to reader agent")
        return "No sources available."
    
    # Validate required columns exist
    required_cols = ["title", "url", "snippet", "reliability_score"]
    if not all(col in sources_df.columns for col in required_cols):
        logger.error(f"Missing required columns. Have: {sources_df.columns.tolist()}")
        return "Invalid source data structure."
    
    # Get top 2 sources by reliability
    try:
        top_sources = sources_df.nlargest(2, "reliability_score")[["title", "url", "snippet"]].to_string(index=False)
        chain = reader_chain()
        result = chain.invoke({"sources": top_sources})
        return result
    except Exception as e:
        logger.error(f"Reader agent failed: {e}")
        return f"Error reading sources: {str(e)}"

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