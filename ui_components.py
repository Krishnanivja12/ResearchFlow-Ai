import streamlit as st

def load_css():
    """Inject the complete custom CSS for ResearchMind."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

    /* ── Reset & base ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: #e8e4dc;
    }

    .stApp {
        background: #0a0a0f;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

    /* ── Hero header ── */
    .hero {
        text-align: center;
        padding: 3.5rem 0 2.5rem;
        position: relative;
    }
    .hero-eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #ff8c32;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    .hero h1 {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2.8rem, 6vw, 5rem);
        font-weight: 800;
        line-height: 1.0;
        letter-spacing: -0.03em;
        color: #f0ebe0;
        margin: 0 0 1rem;
    }
    .hero h1 span {
        color: #ff8c32;
    }
    .hero-sub {
        font-size: 1.05rem;
        font-weight: 300;
        color: #a09890;
        max-width: 520px;
        margin: 0 auto;
        line-height: 1.65;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
        margin: 2rem 0;
    }

    /* ── Input card ── */
    .input-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,140,50,0.15);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(8px);
    }

    /* ── Streamlit input overrides ── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,140,50,0.25) !important;
        border-radius: 10px !important;
        color: #f0ebe0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff8c32 !important;
        box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
    }
    .stTextInput > label {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        color: #ff8c32 !important;
        font-weight: 500 !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
        color: #0a0a0f !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.04em !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2.2rem !important;
        cursor: pointer !important;
        transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
        box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
        opacity: 0.95 !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Download Button (White/Visible) ── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #ffffff 0%, #f0ebe0 100%) !important;
        color: #0a0a0f !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.04em !important;
        border: 2px solid rgba(255,140,50,0.3) !important;
        border-radius: 10px !important;
        padding: 0.7rem 2.2rem !important;
        cursor: pointer !important;
        transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
        box-shadow: 0 4px 20px rgba(255,255,255,0.15) !important;
        width: 100%;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(255,255,255,0.25) !important;
        background: linear-gradient(135deg, #ffffff 0%, #ffffff 100%) !important;
        border-color: #ff8c32 !important;
    }
    .stDownloadButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Pipeline step cards ── */
    .step-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s;
    }
    .step-card.active {
        border-color: rgba(255,140,50,0.4);
        background: rgba(255,140,50,0.04);
    }
    .step-card.done {
        border-color: rgba(80,200,120,0.3);
        background: rgba(80,200,120,0.03);
    }
    .step-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        border-radius: 14px 0 0 14px;
        background: rgba(255,255,255,0.05);
        transition: background 0.3s;
    }
    .step-card.active::before { background: #ff8c32; }
    .step-card.done::before   { background: #50c878; }

    .step-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.3rem;
    }
    .step-num {
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.15em;
        color: #ff8c32;
        opacity: 0.7;
    }
    .step-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #f0ebe0;
    }
    .step-status {
        margin-left: auto;
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.1em;
    }
    .status-waiting  { color: #555; }
    .status-running  { color: #ff8c32; }
    .status-done     { color: #50c878; }

    /* ── Result panels ── */
    .result-panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1.8rem 2rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .result-panel-title {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #ff8c32;
        margin-bottom: 1rem;
        padding-bottom: 0.7rem;
        border-bottom: 1px solid rgba(255,140,50,0.15);
    }
    .result-content {
        font-size: 0.92rem;
        line-height: 1.8;
        color: #cdc8bf;
        white-space: pre-wrap;
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Report & feedback panels ── */
    .report-panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,140,50,0.2);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
    }
    .feedback-panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(80,200,120,0.2);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
    }
    .panel-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        padding-bottom: 0.7rem;
    }
    .panel-label.orange {
        color: #ff8c32;
        border-bottom: 1px solid rgba(255,140,50,0.15);
    }
    .panel-label.green {
        color: #50c878;
        border-bottom: 1px solid rgba(80,200,120,0.15);
    }

    /* ── Progress text ── */
    .stSpinner > div { color: #ff8c32 !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,140,50,0.15) !important;
        border-radius: 10px !important;
        color: #f0ebe0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.2s !important;
    }
    .streamlit-expanderHeader:hover {
        background: rgba(255,140,50,0.05) !important;
        border-color: rgba(255,140,50,0.3) !important;
    }
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,140,50,0.1) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1.5rem !important;
        margin-top: -1px !important;
    }
    details summary {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        color: #f0ebe0 !important;
        letter-spacing: 0.02em !important;
        cursor: pointer;
    }
    details[open] summary {
        color: #ff8c32 !important;
    }

    /* ── Section heading ── */
    .section-heading {
        font-family: 'Syne', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #f0ebe0;
        margin: 2rem 0 1rem;
    }

    /* ── Toast-style notice ── */
    .notice {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        color: #605850;
        text-align: center;
        margin-top: 3rem;
        letter-spacing: 0.08em;
    }

    /* ── DataFrame styling ── */
    .stDataFrame {
        background: rgba(255,255,255,0.02) !important;
        border-radius: 10px !important;
    }
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: rgba(255,255,255,0.02) !important;
    }
    .stDataFrame table {
        color: #e8e4dc !important;
    }
    .stDataFrame thead tr th {
        background: rgba(255,140,50,0.1) !important;
        color: #ff8c32 !important;
        font-family: 'DM Mono', monospace !important;
        font-weight: 600 !important;
        border-bottom: 2px solid rgba(255,140,50,0.3) !important;
    }
    .stDataFrame tbody tr:hover {
        background: rgba(255,140,50,0.05) !important;
    }

    /* ── Text Area ── */
    .stTextArea textarea {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,140,50,0.15) !important;
        border-radius: 10px !important;
        color: #e8e4dc !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.85rem !important;
        line-height: 1.6 !important;
    }

    /* ── Info/Warning/Success boxes ── */
    .stAlert {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px !important;
        border-left: 4px solid !important;
        padding: 1.2rem 1.5rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stAlert[data-baseweb="notification"] {
        background: rgba(255,255,255,0.03) !important;
    }
    [data-testid="stNotificationContentInfo"] {
        border-left-color: #4a9eff !important;
    }
    [data-testid="stNotificationContentWarning"] {
        border-left-color: #ffa500 !important;
    }
    [data-testid="stNotificationContentSuccess"] {
        border-left-color: #50c878 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_hero():
    """Display the hero section."""
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Multi-Agent AI System</div>
        <h1>Research<span>Mind</span></h1>
        <p class="hero-sub">
            Six specialized agents collaborate to deliver an accurate, verified research report.
        </p>
    </div>
    """, unsafe_allow_html=True)


def step_card(num: str, title: str, state: str, desc: str = ""):
    """Render a single pipeline step card."""
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>" + desc + "</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)