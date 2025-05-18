import pandas as pd
import streamlit as st

from visualizations import (
    create_distribution_map,
    create_lifecycle_chart,
    create_size_chart,
    create_taxonomy_treemap,
)


def display_beetle_header_image(
    beetle: dict,
) -> None:
    """
    Display beetle header image and name.
    """
    st.markdown(
        f"<h2>{beetle['common_name']} <em>{beetle['scientific_name']}</em></h2>",
        unsafe_allow_html=True,
    )

    url = beetle["image"]
    st.image(
        url,
        caption=f"{beetle['common_name']} ({beetle['scientific_name']})",
        use_container_width=True,
    )


def display_species_info(
    beetle: dict,
) -> None:
    """
    Display species information in a table format.
    """
    taxonomy = beetle["taxonomy"]
    family = taxonomy["family"]["zh"]
    genus = taxonomy["genus"]["zh"]
    origin = ", ".join(beetle["distribution"]["origin"])
    care_stars = "★" * beetle["care_difficulty"] + "☆" * (5 - beetle["care_difficulty"])
    breeding = beetle["breeding"]
    breeding_stars = "★" * breeding["difficulty"] + "☆" * (5 - breeding["difficulty"])
    male = beetle["adult_size_mm"]["male"]
    female = beetle["adult_size_mm"]["female"]
    adult_size = (
        f"♂ {male['min']} - {male['max']} mm / ♀ {female['min']} - {female['max']} mm"
    )

    df = pd.DataFrame(
        [
            [f"{family} / {genus}"],
            [origin],
            [care_stars],
            [breeding_stars],
            [adult_size],
        ],
        index=["分類資訊", "分布地區", "飼養難度", "繁殖難度", "成蟲體長"],
        columns=["內容"],
    )
    st.table(df)


def display_taxonomy(
    beetle: dict,
    beetles_data: list[dict],
):
    """Display taxonomy visualization."""
    current_genus = beetle["taxonomy"]["genus"]["zh"]
    sunburst_fig = create_taxonomy_treemap(beetles_data, current_genus)
    st.plotly_chart(sunburst_fig, use_container_width=True)


def display_distribution(
    beetle: dict,
):
    """Display global distribution map."""
    distribution_map = create_distribution_map(beetle)
    st.plotly_chart(distribution_map, use_container_width=True)


def display_lifecycle(
    beetle: dict,
):
    """Display lifecycle chart."""
    lifecycle_fig = create_lifecycle_chart(beetle)
    st.plotly_chart(lifecycle_fig, use_container_width=True)


def display_size_data(
    beetle: dict,
):
    """Display size data chart."""
    size_fig = create_size_chart(beetle)
    st.plotly_chart(size_fig, use_container_width=True)


def display_beetle_info_card(
    beetle_data: dict,
):
    """Display beetle information card."""
    st.markdown(
        f"""
        <div class="info-card fadeIn">
            <h4>{beetle_data['common_name']}</h4>
            <p>分類資訊: {beetle_data['taxonomy']['family']['zh']} / {beetle_data['taxonomy']['genus']['zh']}</p>
            <p>分布地區: {', '.join(beetle_data['distribution']['origin'])}</p>
            <p>飼養難度: {"★" * beetle_data["care_difficulty"]}{"☆" * (5 - beetle_data["care_difficulty"])}</p>
            <p>繁殖難度: {"★" * beetle_data['breeding']['difficulty']}{"☆" * (5 - beetle_data['breeding']['difficulty'])}</p>
            <p>成蟲體長: ♂ {beetle_data['adult_size_mm']['male']['min']}-{beetle_data['adult_size_mm']['male']['max']}mm / ♀ {beetle_data['adult_size_mm']['female']['min']}-{beetle_data['adult_size_mm']['female']['max']}mm</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
