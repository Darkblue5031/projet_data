from django.shortcuts import render
from django.http import HttpResponse
from .models import Data
from collections import Counter
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd


def about(request):
    return HttpResponse('<h1>This is about me!.</h1>')


def podium(request):
    return HttpResponse('<h1>podiuuuuuuuuu<h1>')


def location(request):
    return HttpResponse('<h1>location<h1>')


from django.shortcuts import render
import csv


def convert_to_minutes(duration):
    if 'min' in duration:
        return int(duration.split()[0])
    elif 'Season' in duration:
        # Supposons que chaque saison a une durée moyenne de 12 épisodes de 45 minutes chacun
        return int(duration.split()[0]) * 12 * 45


def generate_pie_chart(data):
    durations_in_minutes = [convert_to_minutes(entry['duration']) for entry in data]

    labels = ['Short (< 60 min)', 'Medium (60-120 min)', 'Long (> 120 min)']
    short_count = sum(1 for duration in durations_in_minutes if duration is not None and duration < 60)
    medium_count = sum(1 for duration in durations_in_minutes if duration is not None and 60 <= duration <= 120)
    long_count = sum(1 for duration in durations_in_minutes if duration is not None and duration > 120)
    values = [short_count, medium_count, long_count]

    colors = ['#2ca02c', '#ffaa00', '#eb4034']


    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    pie_chart_html = fig.to_html(full_html=False)
    return pie_chart_html


def generate_choropleth_map(data: list[dict[str, str]]):
    country_counts = Counter()

    for entry in data:
        director_string = entry.get('country', '')
        if director_string:
            countries = [country.strip() for country in director_string.split(',')]
            country_counts.update(countries)

    df = pd.DataFrame(list(country_counts.items()), columns=['country', 'country_values'])

    custom_color_scale = [
        (0.00, "rgb(0, 0, 255)"),  # Blue
        (0.01, "rgb(0, 255, 255)"),  # Cyan
        (0.10, "rgb(0, 255, 0)"),  # Green
        (0.15, "rgb(255, 255, 0)"),  # Yellow
        (1.00, "rgb(255, 0, 0)")  # Red
    ]

    fig = px.choropleth(df,
                        locations='country',  # colonne contenant les noms des pays
                        locationmode='country names',
                        color='country_values',  # colonne contenant les valeurs à colorier
                        hover_name='country',  # colonne à afficher lors du survol
                        color_continuous_scale=custom_color_scale,
                        range_color=(0,500),  # plage de couleurs
                        color_continuous_midpoint=50,
                        title='Netflix Titles by Country')

    map_html = pio.to_html(fig, full_html=False, include_plotlyjs=False, default_width="100%", default_height="100%")
    return map_html


def index(request):
    """
    Index page view
    :param request:
    :return:
    """
    with open('netflix_titles.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    if request.method == 'POST':
        filt = request.POST.get('filter')
        if not filt:
            filt = 'title'
        sorted_data = sorted(data, key=lambda x: x[filt])
    else:
        sorted_data = sorted(data, key=lambda x: x['title'])

    pie_chart_html = generate_pie_chart(sorted_data)
    heatmap_html = generate_choropleth_map(sorted_data)

    return render(request, 'html/test.html',
                  {'sorted_data': sorted_data[:10], 'pie_chart_html': pie_chart_html, 'heatmap_html': heatmap_html})

def duration_pie_chart(request):
    """
    View to display pie chart based on duration/count.
    """
    with open('netflix_titles.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    pie_chart_html = generate_pie_chart(data)

    return render(request, 'html/duration_pie_chart.html', {'pie_chart_html': pie_chart_html})


def generate_director_bar_chart(data):
    director_counts = Counter()

    for entry in data:
        director_string = entry.get('director', '')
        if director_string:
            directors = [director.strip() for director in director_string.split(',')]
            director_counts.update(directors)

    top_directors = director_counts.most_common(10)  # Get the top 10 most represented directors
    top_directors.sort(key=lambda x: x[1], reverse=True)  # Sort by count in descending order

    labels = [director for director, count in top_directors]
    values = [count for director, count in top_directors]

    fig = go.Figure(data=[go.Bar(y=labels, x=values, orientation='h')])
    bar_chart_html = fig.to_html(full_html=False)
    return bar_chart_html


def director_bar_chart(request):
    """
    View to display bar chart based on count of titles per director.
    """
    with open('netflix_titles.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    bar_chart_html = generate_director_bar_chart(data)

    return render(request, 'html/director_bar_chart.html', {'bar_chart_html': bar_chart_html})