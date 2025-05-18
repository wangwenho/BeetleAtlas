import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_taxonomy_treemap(
    data: list,
    current_genus: str,
) -> go.Figure:
    """
    Create a treemap visualization of the taxonomy data.
    """
    taxonomy_data = []

    for beetle in data:
        taxonomy = beetle["taxonomy"]
        common_name = beetle["common_name"]

        if taxonomy["genus"]["zh"] in current_genus:
            taxonomy_data.append(
                {
                    "Kingdom": taxonomy["kingdom"]["zh"],
                    "Phylum": taxonomy["phylum"]["zh"],
                    "Class": taxonomy["class"]["zh"],
                    "Order": taxonomy["order"]["zh"],
                    "Family": taxonomy["family"]["zh"],
                    "Subfamily": taxonomy["subfamily"]["zh"],
                    "Genus": taxonomy["genus"]["zh"],
                    "CommonName": common_name,
                }
            )

    df = pd.DataFrame(taxonomy_data)

    fig = px.treemap(
        df,
        path=[
            "Kingdom",
            "Phylum",
            "Class",
            "Order",
            "Family",
            "Subfamily",
            "Genus",
            "CommonName",
        ],
        hover_data=["CommonName"],
        color_discrete_sequence=["#939D5A"] * len(df),
    )
    fig.update_layout(
        title={
            "text": f"{current_genus}的其他物種",
            "x": 0.5,
            "xanchor": "center",
        },
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def create_distribution_map(
    beetle_data: dict,
) -> go.Figure:
    """
    Create a choropleth map showing the distribution of the beetle species.
    """
    countries = beetle_data["distribution"]["countries"]

    values = [1] * len(countries)

    fig = go.Figure(
        go.Choropleth(
            locations=countries,
            z=values,
            locationmode="ISO-3",
            colorscale=[[0, "#737C42"], [1, "#737C42"]],
            showscale=False,
            marker_line_color="#585D3D",
            text=None,
        )
    )

    fig.update_geos(
        projection_type="equirectangular",
        showcountries=True,
        countrycolor="#A5A492",
        showland=True,
        landcolor="#EAE9E6",
        showocean=True,
        oceancolor="#9DC8D1",
        bgcolor="#EAE9E6",
    )

    fig.update_layout(
        title={
            "text": f"{beetle_data['common_name']}的全球分布",
            "x": 0.5,
            "xanchor": "center",
        },
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig


def create_size_chart(
    beetle_data: dict,
) -> go.Figure:
    """
    Create a box plot showing the size data of the beetle species.
    """
    adult_size = beetle_data["adult_size_mm"]

    male_min = adult_size["male"]["min"]
    male_max = adult_size["male"]["max"]
    female_min = adult_size["female"]["min"]
    female_max = adult_size["female"]["max"]

    male_median = (male_min + male_max) / 2
    male_q1 = male_min + (male_max - male_min) * 0.25
    male_q3 = male_min + (male_max - male_min) * 0.75

    female_median = (female_min + female_max) / 2
    female_q1 = female_min + (female_max - female_min) * 0.25
    female_q3 = female_min + (female_max - female_min) * 0.75

    fig = go.Figure()

    fig.add_trace(
        go.Box(
            x=[male_min, male_q1, male_median, male_q3, male_max],
            name="雄性",
            boxpoints=False,
            marker_color="#737C42",
            line_width=2,
        )
    )

    fig.add_trace(
        go.Box(
            x=[female_min, female_q1, female_median, female_q3, female_max],
            name="雌性",
            boxpoints=False,
            marker_color="#939D5A",
            line_width=2,
        )
    )

    fig.update_layout(
        title={
            "text": f"{beetle_data['common_name']}的體長數據",
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis_title="體長 (mm)",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        boxmode="group",
    )

    return fig


def create_lifecycle_chart(
    beetle_data: dict,
) -> go.Figure:
    """
    Create a pie chart showing the lifecycle of the beetle species.
    """
    breeding = beetle_data["breeding"]

    male_total = (
        breeding["larval_period_months"]["male"]
        + breeding["adult_lifespan_months"]["male"]
    )
    female_total = (
        breeding["larval_period_months"]["female"]
        + breeding["adult_lifespan_months"]["female"]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            values=[
                breeding["larval_period_months"]["female"],
                breeding["adult_lifespan_months"]["female"],
            ],
            labels=["幼蟲期", "成蟲期"],
            domain=dict(x=[0, 0.45]),
            hole=0.6,
            marker_colors=["#939D5A", "#737C42"],
            sort=False,
            textinfo="label+value",
            textposition="inside",
            hoverinfo="label+percent+value",
            name="雌性",
            title=f"雌性（{female_total} 個月）",
        )
    )

    fig.add_trace(
        go.Pie(
            values=[
                breeding["larval_period_months"]["male"],
                breeding["adult_lifespan_months"]["male"],
            ],
            labels=["幼蟲期", "成蟲期"],
            domain=dict(x=[0.55, 1]),
            hole=0.6,
            marker_colors=["#939D5A", "#737C42"],
            sort=False,
            textinfo="label+value",
            textposition="inside",
            hoverinfo="label+percent+value",
            name="雄性",
            title=f"雄性（{male_total} 個月）",
        )
    )

    fig.update_layout(
        title={
            "text": f"{beetle_data['common_name']}的生命週期",
            "x": 0.5,
            "xanchor": "center",
        },
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
    )

    return fig
