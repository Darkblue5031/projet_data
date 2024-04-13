"""
Functions for generating visualizations for the Netflix Dashboard.
"""

from collections import Counter
from os.path import expanduser

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio

df = pd.read_csv("netflix_titles.csv")


def ratio(col: str, value: str) -> float:
    """
    Calculer le ratio de la colonne spécifiée par rapport à la valeur spécifiée.
    :param col:
    :param value:
    :return:
    """
    count = (df[col] == value).sum()
    lengh_col = len(df)

    return (count / lengh_col) * 100


def convert_to_minutes(duration: str) -> int | None:
    """
    Convertir la durée de visionnage en minutes.
    :param duration:
    :return:
    """
    if "min" in duration:
        return int(duration.split()[0])
    if "Season" in duration:
        return int(duration.split()[0]) * 12 * 45


def generate_pie_chart(data):
    """
    Générer un graphique circulaire basé sur la durée de visionnage.
    :param data:
    :return:
    """
    durations_in_minutes = [convert_to_minutes(entry["duration"]) for entry in data]

    labels = ["Short (< 60 min)", "Medium (60-120 min)", "Long (> 120 min)"]
    short_count = sum(
        1 for duration in durations_in_minutes if duration is not None and duration < 60
    )
    medium_count = sum(
        1
        for duration in durations_in_minutes
        if duration is not None and 60 <= duration <= 120
    )
    long_count = sum(
        1
        for duration in durations_in_minutes
        if duration is not None and duration > 120
    )
    values = [short_count, medium_count, long_count]

    colors = ["#2ca02c", "#ffaa00", "#eb4034"]

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=values, marker={"colors": colors})]
    )
    pie_chart_html = fig.to_html(full_html=False)
    return pie_chart_html


def generate_choropleth_map_duration(data: list[dict[str, str]], typ: str = "Movie"):
    """
    Générer une carte choroplèthe basée sur la durée moyenne de visionnage par pays.
    :param data:
    :param typ:
    :return:
    """
    # Utilisez Counter pour compter la somme des durées de visionnage par pays
    country_durations = Counter()

    # Parcourir chaque entrée dans les données
    for entry in data:
        if entry.get("type", "") != typ:
            continue
        countries_string = entry.get("country", "")
        if countries_string:  # Vérifier si la chaîne de pays n'est pas vide
            # Diviser les noms de pays en une liste de pays individuels
            countries = [country.strip() for country in countries_string.split(",")]
            # Somme des durées de visionnage pour chaque pays
            duration = entry.get("duration", "")
            if duration:
                minutes = convert_to_minutes(duration)
                for country in countries:
                    if country == "Soviet Union":
                        country_durations["Russia"] += minutes
                    else:
                        country_durations[country] += minutes

    # Calcul de la durée moyenne de visionnage par pays
    country_avg_durations = {}
    for country, total_duration in country_durations.items():
        count_titles = sum(
            1
            for entry in data
            if country in entry.get("country", "") and entry.get("type", "") == typ
        )
        if country == "Russia" and typ == "Movie":
            count_titles += 3
        avg_duration = total_duration / count_titles if count_titles > 0 else 0
        if country == "Russia":
            print(total_duration, count_titles, avg_duration)

        country_avg_durations[country] = avg_duration

    local_df = pd.DataFrame(
        list(country_avg_durations.items()), columns=["country", "avg_duration"]
    )

    fig = px.choropleth(
        local_df,
        locations="country",
        locationmode="country names",
        color="avg_duration",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="country average duration",
        range_color=(0, max(local_df["avg_duration"])),
    )

    # Convertir la figure en HTML
    map_html = pio.to_html(fig, full_html=False, include_plotlyjs=False)
    return map_html


def generate_choropleth_map(
    data: list[dict[str, str]],
    title: str = "Netflix Titles by Country",
    col: str = "country",
):
    """
    Générer une carte choroplèthe bas
    :param data:
    :param title:
    :param col:
    :return:
    """
    # Utilisez Counter pour compter les occurrences de chaque pays
    country_counts = Counter()

    for entry in data:
        director_string = entry.get("country", "")
        if director_string:
            countries = [country.strip() for country in director_string.split(",")]
            country_counts.update(countries)

    local_df = pd.DataFrame(
        list(country_counts.items()), columns=["country", "country_values"]
    )

    custom_color_scale = [
        (0.00, "rgb(0, 0, 255)"),  # Blue
        (0.01, "rgb(0, 255, 255)"),  # Cyan
        (0.10, "rgb(0, 255, 0)"),  # Green
        (0.15, "rgb(255, 255, 0)"),  # Yellow
        (1.00, "rgb(255, 0, 0)"),  # Red
    ]

    fig = px.choropleth(
        local_df,
        locations=col,
        locationmode="country names",
        color="country_values",
        hover_name=col,
        color_continuous_scale=custom_color_scale,
        range_color=(0, 500),
        color_continuous_midpoint=50,
        title=title,
    )

    map_html = pio.to_html(fig, full_html=False, include_plotlyjs=False)
    return map_html


def generate_director_bar_chart(data):
    """

    :param data:
    :return:
    """
    director_counts = Counter()

    for entry in data:
        director_string = entry.get("director", "")
        if director_string:
            directors = [director.strip() for director in director_string.split(",")]
            director_counts.update(directors)

    top_directors = director_counts.most_common(
        10
    )  # Get the top 10 most represented directors
    top_directors.sort(
        key=lambda x: x[1], reverse=True
    )  # Sort by count in descending order

    labels = [director for director, count in top_directors]
    values = [count for director, count in top_directors]

    fig = go.Figure(data=[go.Bar(y=labels, x=values, orientation="h")])
    bar_chart_html = fig.to_html(full_html=False)
    return bar_chart_html


def generate_cast_bar_chart(data: list, top_n: int = 100, typ: str = "Movie"):
    """
    Generate a bar chart based on the count of titles per cast member.
    :param typ:
    :param data:
    :param top_n:
    :return:
    """
    df = pd.DataFrame(data)
    df = df[df["cast"].notnull() & (df["cast"] != "") & (df["type"] == typ)]

    if df.empty:
        return "No data available with non-empty cast."

    cast_counts = df["cast"].str.split(", ", expand=True).stack().value_counts()
    top_cast = cast_counts.head(top_n)

    cast_df = pd.DataFrame({"cast": top_cast.index, "count": top_cast.values})

    type_col = df["type"].iloc[0]
    title = f"Top 10 Cast Members in {type_col}s by Number of Titles"
    fig = px.bar(cast_df, x="cast", y="count", title=title)

    return fig.to_html(full_html=False)


def avg_duration(duration: int, count) -> int:
    """
    Calculer la durée moyenne par titre.
    :param duration:
    :param count:
    :return:
    """
    return duration / count


def generate_cast_duration_bar_chart(data: list, top_n: int = 100, typ: str = "Movie"):
    """
    Generate a bar chart based on the average duration of titles per cast member.
    :param data: List of dictionaries containing title data.
    :param top_n: Number of top cast members to include in the chart.
    :param typ: Type of titles to consider (e.g., "Movie" or "TV Show").
    :return: HTML code for the generated plot.
    """
    df = pd.DataFrame(data)
    df = df[df["cast"].notnull() & (df["cast"] != "") & (df["type"] == typ)]
    if df.empty:
        return "No data available with non-empty cast."

    print()

    # Split and explode the 'cast' column
    cast_counts = df["cast"].str.split(", ", expand=True).stack().value_counts()
    df["cast"] = df["cast"].str.split(", ", expand=True).stack().explode("cast")

    # Convert duration to minutes
    df["duration_minutes"] = df["duration"].apply(convert_to_minutes)

    # Calculate the total duration for each cast member
    cast_duration = df.groupby("cast")["duration_minutes"].sum()

    # Calculate the total number of titles for each cast member
    cast_count = df.groupby("cast").size()

    # Calculate the average duration for each cast member
    cast_avg_duration = cast_duration / cast_count

    # Create a DataFrame with cast members and their average duration
    cast_df = pd.DataFrame(
        {"cast": cast_avg_duration.index, "avg_duration": cast_avg_duration.values}
    )

    # Sort the DataFrame by average duration in descending order
    cast_df = cast_df.sort_values(by="avg_duration", ascending=False)

    # Select the top N cast members
    cast_df = cast_df.head(top_n)

    # Create the bar chart

    fig = px.bar(
        cast_df,
        x="cast",
        y="avg_duration",
        title=f"Top {top_n} Cast Members in {typ}s by Average Duration",
        labels={"avg_duration": "Average Duration (minutes)"},
    )

    return fig.to_html(full_html=False)
