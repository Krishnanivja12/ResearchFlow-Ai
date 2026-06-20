import pandas as pd
import streamlit as st

def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Convert a DataFrame to a markdown table."""
    return df.to_markdown(index=False) if not df.empty else "No data."

@st.cache_data
def convert_report_to_pdf(md_content: str) -> bytes:
    """Convert markdown report to PDF (requires pdfkit)."""
    # For simplicity, return a placeholder – can be implemented later
    import markdown
    html = markdown.markdown(md_content)
    # pdfkit.from_string(html, 'report.pdf') ... 
    return b"PDF placeholder"