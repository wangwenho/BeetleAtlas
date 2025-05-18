from pathlib import Path

import streamlit as st


def apply_styles(
    css_file_path: str | Path = "static/styles.css",
) -> None:
    """
    Apply custom styles to the Streamlit app.
    """
    with Path(css_file_path).open("r", encoding="utf-8") as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def set_page_config(
    page_title: str = "互動式甲蟲圖鑑",
    page_icon: str = "🪲",
    layout: str = "wide",
):
    """
    Set the page configuration for the Streamlit app.
    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
    )
