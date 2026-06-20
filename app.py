import streamlit as st
from ui_components import load_css, render_hero, step_card
from pipeline import ResearchPipeline
from agents import (
    run_search, parse_search_results, run_reader,
    run_writer, run_critic, run_fact_checker, run_summarizer
)

# ── Page Config & Styles ────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_css()

# ── Session State Initialisation ────────────────────────────────────────────
defaults = {
    "results": {},
    "pipeline": None,
    "done": False,
    "manual_mode": False,        # True if user clicked "Step-by-Step"
    "step_index": 0,             # which step to execute next
    "topic": "",
    "sources_df": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Pipeline Step Definitions ───────────────────────────────────────────────
# Order and display names + execution functions
PIPELINE_STEPS = [
    ("Search Agent",     run_search),
    ("Reader Agent",     run_reader),
    ("Writer Agent",     run_writer),
    ("Critic Agent",     run_critic),
    ("Fact Checker",     run_fact_checker),
    ("Summarizer",       run_summarizer),
]

# ── Helper: Render Pipeline Status with cards ───────────────────────────────
def render_pipeline_status():
    """Show step cards reflecting current state (waiting/running/done)."""
    for i, (name, _) in enumerate(PIPELINE_STEPS):
        idx = i  # 0‑based
        if st.session_state.done:
            state = "done"
        elif st.session_state.manual_mode:
            # Manual mode: only the current step_index is running, previous are done
            if idx < st.session_state.step_index:
                state = "done"
            elif idx == st.session_state.step_index and st.session_state.step_index < len(PIPELINE_STEPS):
                state = "running"
            else:
                state = "waiting"
        else:
            # Auto mode: if pipeline running and not done, all steps are waiting
            state = "waiting"
        step_card(f"{i+1:02d}", name, state)

# ── Main UI ─────────────────────────────────────────────────────────────────
render_hero()
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 4], gap="large")
with col1:
    st.session_state.topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs 2025",
        key="topic_input",
        label_visibility="visible",
    )
    auto_btn = st.button("⚡ Run Full Pipeline", use_container_width=True)
    step_btn = st.button("🔍 Step‑by‑Step", use_container_width=True)

with col2:
    st.markdown("### Pipeline Status")
    render_pipeline_status()
    if st.session_state.done:
        step_card("07", "Pipeline Complete", "done")

# ── Button Handlers ─────────────────────────────────────────────────────────
def start_auto_pipeline():
    """Reset for full automatic run."""
    st.session_state.results = {}
    st.session_state.pipeline = ResearchPipeline(st.session_state.topic)
    st.session_state.done = False
    st.session_state.manual_mode = False
    st.session_state.step_index = 0
    st.session_state.sources_df = None

def start_manual_pipeline():
    """Reset for step‑by‑step mode."""
    st.session_state.results = {}
    st.session_state.pipeline = ResearchPipeline(st.session_state.topic)
    st.session_state.done = False
    st.session_state.manual_mode = True
    st.session_state.step_index = 0
    st.session_state.sources_df = None

if auto_btn and st.session_state.topic.strip():
    start_auto_pipeline()
    st.rerun()
elif auto_btn and not st.session_state.topic.strip():
    st.warning("Please enter a research topic.")

if step_btn and st.session_state.topic.strip():
    start_manual_pipeline()
    st.rerun()
elif step_btn and not st.session_state.topic.strip():
    st.warning("Please enter a research topic.")

# ── Execution Logic ─────────────────────────────────────────────────────────

def execute_next_step():
    """Run the agent corresponding to the current step_index (manual mode)."""
    idx = st.session_state.step_index
    if idx >= len(PIPELINE_STEPS):
        st.session_state.done = True
        return

    step_name, step_func = PIPELINE_STEPS[idx]
    results = st.session_state.results
    topic = st.session_state.topic

    try:
        with st.spinner(f"{step_name} is working…"):
            if step_name == "Search Agent":
                raw = step_func(topic)
                results["search"] = raw
                # parse and store dataframe
                df = parse_search_results(raw)
                st.session_state.sources_df = df

            elif step_name == "Reader Agent":
                # use the search results to feed the reader
                search_raw = results.get("search", "")
                # If we have a dataframe, use it; else empty
                df = st.session_state.sources_df
                if df is not None and not df.empty:
                    reader_output = run_reader(df)
                else:
                    reader_output = "No sources available."
                results["reader"] = reader_output

            elif step_name == "Writer Agent":
                research = f"SEARCH RESULTS:\n{results.get('search', '')}\n\nDETAILED CONTENT:\n{results.get('reader', '')}"
                results["writer"] = run_writer(topic, results.get("search", ""), results.get("reader", ""))

            elif step_name == "Critic Agent":
                report = results.get("writer", "")
                results["critic"] = run_critic(report)

            elif step_name == "Fact Checker":
                report = results.get("writer", "")
                sources = results.get("search", "")
                results["fact_checker"] = run_fact_checker(report, sources)

            elif step_name == "Summarizer":
                report = results.get("writer", "")
                results["summary"] = run_summarizer(report)

        # After successful execution, move to next step
        st.session_state.step_index += 1
        st.session_state.results = results

    except Exception as e:
        st.error(f"{step_name} failed: {e}")
        st.session_state.done = True   # stop the pipeline on error

def execute_auto_pipeline():
    """Run all agents sequentially (for full auto mode)."""
    pipeline = st.session_state.pipeline
    with st.spinner("Research in progress…"):
        try:
            all_results = pipeline.execute_all()
            st.session_state.results = all_results
            # retrieve the sources_df if stored by the pipeline
            if hasattr(pipeline, "sources_df"):
                st.session_state.sources_df = pipeline.sources_df
        except Exception as e:
            st.error(f"Pipeline error: {e}")
    st.session_state.done = True

# ── Manual Mode Runner ──
if st.session_state.manual_mode and not st.session_state.done:
    # If we still have steps to execute, show a button to trigger the next one
    if st.session_state.step_index < len(PIPELINE_STEPS):
        if st.button("▶️ Execute Next Step", use_container_width=True):
            execute_next_step()
            st.rerun()
    else:
        st.session_state.done = True
        st.rerun()

# ── Auto Mode Runner ──
if not st.session_state.manual_mode and st.session_state.pipeline is not None and not st.session_state.done:
    execute_auto_pipeline()
    st.rerun()

# ── Display Results ─────────────────────────────────────────────────────────
if st.session_state.done and st.session_state.results:
    r = st.session_state.results
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📊 Research Results")

    # Search Results in Dropdown
    if "search" in r:
        with st.expander("🔍 Search Results - Real-Time Sources", expanded=False):
            st.markdown("**Found Sources from Tavily API:**")
            if st.session_state.sources_df is not None and not st.session_state.sources_df.empty:
                # Display as a nice table
                df = st.session_state.sources_df
                st.dataframe(
                    df,
                    use_container_width=True,
                    column_config={
                        "url": st.column_config.LinkColumn("URL"),
                        "reliability_score": st.column_config.NumberColumn(
                            "Reliability",
                            help="Score from 1-10",
                            format="%.0f ⭐"
                        )
                    }
                )
            else:
                st.json(r["search"])

    # Reader Content in Dropdown
    if "reader" in r:
        with st.expander("📄 Scraped Content - Detailed Information", expanded=False):
            st.markdown("**Content extracted from top sources:**")
            st.text_area("Reader Output", r["reader"], height=300, label_visibility="collapsed")

    # Main Report (always visible)
    if "writer" in r:
        st.markdown("### 📝 Final Research Report")
        st.markdown(r["writer"])
        
        # White Download Button
        st.download_button(
            label="⬇️ Download Report (Markdown)",
            data=r["writer"],
            file_name=f"research_report_{st.session_state.topic.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # Critic Feedback in Dropdown
    if "critic" in r:
        with st.expander("🧐 Critic Feedback - Quality Review", expanded=False):
            st.info(r["critic"])

    # Fact-Check Results in Dropdown
    if "fact_checker" in r:
        with st.expander("✅ Fact-Check Results - Source Verification", expanded=False):
            st.warning(r["fact_checker"])

    # Executive Summary (highlighted)
    if "summary" in r:
        st.markdown("### 📑 Executive Summary")
        st.success(r["summary"])