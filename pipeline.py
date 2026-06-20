from dataclasses import dataclass, field
from typing import Dict
import streamlit as st
from agents import (
    run_search, parse_search_results, run_reader, run_writer,
    run_critic, run_fact_checker, run_summarizer
)

@dataclass
class ResearchPipeline:
    topic: str
    results: Dict[str, str] = field(default_factory=dict)

    def execute_all(self):
        """Run all agents sequentially, updating the results dict."""
        # 1. Search
        self.results["search"] = run_search(self.topic)
        # 2. Parse into DataFrame (store as string for display)
        df = parse_search_results(self.results["search"])
        self.results["sources_df"] = df  
        # 3. Reader
        self.results["reader"] = run_reader(df)
        # 4. Writer
        self.results["writer"] = run_writer(self.topic, self.results["search"], self.results["reader"])
        # 5. Critic
        self.results["critic"] = run_critic(self.results["writer"])
        # 6. Fact Checker (uses original search results)
        self.results["fact_checker"] = run_fact_checker(self.results["writer"], self.results["search"])
        # 7. Summarizer
        self.results["summary"] = run_summarizer(self.results["writer"])
        return self.results