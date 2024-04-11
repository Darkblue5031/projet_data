from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .func import ratio

def about(request):
    return HttpResponse('<h1>This is about me!.</h1>')

def podium(request):
    return HttpResponse('<h1>podiuuuuuuuuu<h1>')

def location(request):
    return HttpResponse('<h1>location<h1>')

def index(request):
    context = {
        '%movie': ratio("type", "Movie"),
    }

    return render(request, 'html/test.html', context=context)

def display_csv_data(request):
    csv_path = 'netflix_titles.csv'
    df = pd.read_csv(csv_path)
    data = df.to_dict(orient='records')
    headers = df.columns
    return render(request, 'html/test.html', {'headers': headers, 'data': data})

