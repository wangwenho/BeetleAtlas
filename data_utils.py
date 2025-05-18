import json
from pathlib import Path

import streamlit as st


@st.cache_data
def load_data(
    data_dir: str | Path = "beetles",
):
    return [
        json.load(open(file, "r", encoding="utf-8"))
        for file in Path(data_dir).rglob("*.json")
    ]
