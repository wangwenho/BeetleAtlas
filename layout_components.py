import numpy as np
import streamlit as st

from ui_components import (
    display_beetle_header_image,
    display_beetle_info_card,
    display_distribution,
    display_lifecycle,
    display_size_data,
    display_species_info,
    display_taxonomy,
)


def sidebar_search_filter(
    beetles_data: list[dict],
) -> tuple[dict, list[str], dict[str, int], int]:
    """
    Sidebar search and filter for beetles.
    """
    with st.sidebar:
        st.markdown("# 🪲互動式甲蟲圖鑑")
        st.markdown(
            """
            <p>這是一個互動式的甲蟲圖鑑，你可以輕鬆探索不同種類的甲蟲。</p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("## 🔍 搜尋甲蟲")

        all_names = [
            f"{beetle['common_name']} ({beetle['scientific_name']})"
            for beetle in beetles_data
        ]
        name_to_index = {name: idx for idx, name in enumerate(all_names)}
        default_index = st.session_state.get("random_index", 0)

        selected_name = st.selectbox(
            "以俗名或學名搜尋",
            options=all_names,
            index=default_index,
            key="beetle_selectbox",
        )

        selected_index = name_to_index[selected_name]
        selected_beetle = beetles_data[selected_index]

        filtered_beetles = handle_advanced_filtering(beetles_data)

        if st.button("🎲 隨機探索"):
            if filtered_beetles:
                random_beetle = np.random.choice(filtered_beetles)
                st.session_state.random_index = beetles_data.index(random_beetle)

        return selected_beetle, all_names, name_to_index, selected_index


def handle_advanced_filtering(
    beetles_data: list[dict],
) -> list[dict]:
    """
    Handle advanced filtering of beetles.
    """
    st.markdown("## 🗄️ 進階篩選")

    with st.expander("顯示篩選選項", expanded=False):
        all_families = list(
            set([beetle["taxonomy"]["genus"]["zh"] for beetle in beetles_data])
        )
        selected_genus = st.multiselect("按屬過濾", all_families)

        difficulty_filter = st.select_slider(
            "飼養難度",
            options=[1, 2, 3, 4, 5],
            value=(1, 5),
        )

        filtered_beetles = beetles_data
        if selected_genus:
            filtered_beetles = [
                beetle
                for beetle in filtered_beetles
                if beetle["taxonomy"]["genus"]["zh"] in selected_genus
            ]
        filtered_beetles = [
            beetle
            for beetle in filtered_beetles
            if difficulty_filter[0] <= beetle["care_difficulty"] <= difficulty_filter[1]
        ]

        st.write(f"符合條件的甲蟲: {len(filtered_beetles)} 種")

    return filtered_beetles


def display_beetle_details(
    selected_beetle: dict,
    beetles_data: list[dict],
):
    """
    Display beetle details.
    """
    with st.container():
        st.markdown("### 💡 甲蟲詳情")
        col1, col2 = st.columns([4, 6])

        with col1:
            display_beetle_header_image(selected_beetle)

        with col2:
            display_beetle_tabs(selected_beetle, beetles_data)


def display_beetle_tabs(
    beetle: dict,
    beetles_data: list[dict],
) -> None:
    """
    Display beetle tabs for detailed information.
    """
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📋 物種資訊",
            "👀 分類系統",
            "🌍 全球分布",
            "⏳ 生命週期",
            "📏 體長數據",
        ]
    )

    with tab1:
        display_species_info(beetle)

    with tab2:
        display_taxonomy(beetle, beetles_data)

    with tab3:
        display_distribution(beetle)

    with tab4:
        display_lifecycle(beetle)

    with tab5:
        display_size_data(beetle)


def display_beetle_comparison(
    beetles_data: list[dict],
    all_names: list[str],
    name_to_index: dict[str, int],
    selected_index: int,
) -> None:
    """
    Display beetle comparison section.
    """
    with st.container():
        st.markdown("### 🔄 甲蟲比較")

        col1, col2 = st.columns(2)

        with col1:
            compare_beetle1 = st.selectbox(
                "選擇第一種甲蟲",
                options=all_names,
                index=selected_index,
                key="compare_beetle1",
            )
            beetle1_index = name_to_index[compare_beetle1]
            beetle1_data = beetles_data[beetle1_index]

            display_beetle_info_card(beetle1_data)

        with col2:
            compare_beetle2 = st.selectbox(
                "選擇第二種甲蟲",
                options=[n for n in all_names if n != compare_beetle1],
                index=0,
                key="compare_beetle2",
            )
            beetle2_index = name_to_index[compare_beetle2]
            beetle2_data = beetles_data[beetle2_index]

            display_beetle_info_card(beetle2_data)
