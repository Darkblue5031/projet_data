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
