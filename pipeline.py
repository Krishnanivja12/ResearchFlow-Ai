from dataclasses import dataclass, field
from typing import Dict, Any
import pandas as pd
from agents import (
    run_search, parse_search_results, run_reader, run_writer,
    run_critic, run_fact_checker, run_summarizer
)

@dataclass
class ResearchPipeline:
    topic: str
    results: Dict[str, Any] = field(default_factory=dict)
    sources_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    def execute_all(self):
        """Run all agents sequentially, updating the results dict."""
        # 1. Search
        self.results["search"] = run_search(self.topic)
        # 2. Parse into DataFrame and store as instance attribute
        self.sources_df = parse_search_results(self.results["search"])
        # 3. Reader
        self.results["reader"] = run_reader(self.sources_df)
        # 4. Writer
        self.results["writer"] = run_writer(self.topic, self.results["search"], self.results["reader"])
        # 5. Critic
        self.results["critic"] = run_critic(self.results["writer"])
        # 6. Fact Checker (uses original search results)
        self.results["fact_checker"] = run_fact_checker(self.results["writer"], self.results["search"])
        # 7. Summarizer
        self.results["summary"] = run_summarizer(self.results["writer"])
        return self.results