from django.shortcuts import render
from django.http import HttpResponse
from .models import Data


def about(request):
    return HttpResponse('<h1>This is about me!.</h1>')


def podium(request):
    return HttpResponse('<h1>podiuuuuuuuuu<h1>')


def location(request):
    return HttpResponse('<h1>location<h1>')


from django.shortcuts import render
import csv


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
    return render(request, 'html/test.html', {'sorted_data': sorted_data[:10]})
