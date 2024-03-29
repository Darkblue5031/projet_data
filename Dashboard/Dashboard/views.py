from django.shortcuts import render
from django.http import HttpResponse
from .models import Data

def about(request):
    return HttpResponse('<h1>This is about me!.</h1>')

def podium(request):
    return HttpResponse('<h1>podiuuuuuuuuu<h1>')

def location(request):
    return HttpResponse('<h1>location<h1>')

def index(request):
    genders = Data.objects.values_list('Gender', flat=True)
    ages = Data.objects.values_list("Age", flat=True)

    num_books = 15
    num_instances = 20

    print(ages)
    print(genders)

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'genders': genders,
        'ages': ages,
    }
    return render(request, 'html/base.html', context=context)