"""
Views for the dashboard app.
"""

from csv import DictReader
from django.http import HttpResponse
from django.shortcuts import render
from . import func


def about(request):
    """
    View to display about me.
    :param request:
    :return:
    """
    return HttpResponse("<h1>This is about me!.</h1>")


def podium(request):
    """
    View to display podium.
    :param request:
    :return:
    """
    return HttpResponse("<h1>podiuuuuuuuuu<h1>")


def location(request):
    """
    View to display location.
    :param request:
    :return:
    """
    return HttpResponse("<h1>location<h1>")


def duration_pie_chart(request):
    """
    View to display pie chart based on duration/count.
    """
    with open("netflix_titles.csv", newline="", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        data = list(reader)

    pie_chart_html = func.generate_pie_chart(data)

    return render(
        request, "html/duration_pie_chart.html", {"pie_chart_html": pie_chart_html}
    )


def director_bar_chart(request):
    """
    View to display bar chart based on count of titles per director.
    """
    with open("netflix_titles.csv", newline="", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        data = list(reader)

    bar_chart_html = func.generate_director_bar_chart(data)

    return render(
        request, "html/director_bar_chart.html", {"bar_chart_html": bar_chart_html}
    )


def cast_bar_chart(request):
    """
    View to display bar chart based on count of titles per cast.
    """
    with open("netflix_titles.csv", newline="", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        data = list(reader)

    bar_chart_html = func.generate_cast_bar_chart(data)
    bar_chart_html1 = func.generate_cast_bar_chart(data, typ="TV Show")
    bar_chart_html2 = func.generate_cast_duration_bar_chart(data)
    bar_chart_html3 = func.generate_cast_duration_bar_chart(data, typ="TV Show")

    return render(
        request,
        "html/cast_bar_chart.html",
        {
            "bar_chart_html": bar_chart_html,
            "bar_chart_html1": bar_chart_html1,
            "bar_chart_html2": bar_chart_html2,
            "bar_chart_html3": bar_chart_html3,
        },
    )

def generate_pie_chart(data):
    durations_in_minutes = [convert_to_minutes(entry['duration']) for entry in data]

def cast_line_chart(request):
    """
    View to display line chart based on count of titles per cast.
    :param request:
    :return:
    """
    with open("netflix_titles.csv", newline="", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        data = list(reader)
    line_chart_html = func.generate_release_year_line_chart(data)
    line_chart_html1 = func.generate_release_year_line_chart(data, typ="TV Show")
    return render(
        request,
        "html/cast_line_chart.html",
        {"line_chart_html": line_chart_html, "line_chart_html1": line_chart_html1},
    )

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=['#E4101F', '#AD0C11', '#960c10']))],
                layout=go.Layout(
                    paper_bgcolor='#211C19',
                    plot_bgcolor='#211C19',
                    font=dict(color='#FAFAFA'),
                    title='Netflix average duration',
                ))
    pie_chart_html = fig.to_html(full_html=False)
    return pie_chart_html

def cast_circular_chart(request):
    """

    :param request:
    :return:
    """
    with open("netflix_titles.csv", newline="", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        data = list(reader)
    circular_chart_html = func.generate_listed_in_circular_chart(data)
    circular_chart_html1 = func.generate_listed_in_circular_chart(data, typ="TV Show")
    return render(
        request,
        "html/cast_circular_chart.html",
        {
            "circular_chart_html": circular_chart_html,
            "circular_chart_html1": circular_chart_html1,
        },
    )

    # Créez une dataframe à partir des données de pays et de leurs occurrences
    df = pd.DataFrame(list(country_counts.items()), columns=['country', 'country_values'])

    # Utilisez Plotly Express pour créer la carte choroplèthe
    fig = px.choropleth(df,
                        locations='country',  # colonne contenant les noms des pays
                        locationmode='country names',
                        color='country_values',  # colonne contenant les valeurs à colorier
                        hover_name='country',  # colonne à afficher lors du survol
                        color_continuous_scale=['#E4101F', '#960c10', '#211C19'],
                        range_color=(0, 100),  # plage de couleurs
                        title='Netflix Titles by Country',
                        )
    fig.update_layout(
        paper_bgcolor='#211C19',
        plot_bgcolor='#211C19',
        font=dict(color='#FAFAFA'),
    )

def duration_line_chart(request):
    """
    View to display line chart based on duration/count.
    """
    with open("netflix_titles.csv", newline="", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        data = list(reader)

    line_chart_html = func.generate_duration_line_chart(data)
    line_chart_html1 = func.generate_duration_line_chart(data, typ="TV Show")

    return render(
        request,
        "html/duration_line_chart.html",
        {"line_chart_html": line_chart_html, "line_chart_html1": line_chart_html1},
    )


def index(request):
    """
    Index page view
    :param request:
    :return:
    """
    with open("netflix_coord.csv", newline="", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        data = list(reader)
    if request.method == "POST":
        filt = request.POST.get("filter")
        if not filt:
            filt = "title"
        sorted_data = sorted(data, key=lambda x: x[filt])
    else:
        sorted_data = sorted(data, key=lambda x: x["title"])

    pie_chart_html = func.generate_pie_chart(sorted_data)
    heatmap_html = func.generate_choropleth_map(sorted_data)
    duration_map = func.generate_choropleth_map_duration(sorted_data)

    return render(
        request,
        "html/test.html",
        {
            "pie_chart_html": pie_chart_html,
            "heatmap_html": heatmap_html,
            "duration_map": duration_map,
        },
    )
