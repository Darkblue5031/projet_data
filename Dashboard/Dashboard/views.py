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
    # Open the CSV file
    with open('netflix_titles.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Read the CSV data into a list of dictionaries
        data = [row for row in reader]

    # Sort the data by the 'title' key
    sorted_data = sorted(data, key=lambda x: x['title'])

    # Pass the sorted data to the template
    return render(request, 'html/test.html', {'sorted_data': sorted_data})
