from django.shortcuts import render
from django.http import HttpResponse

def about(request):
    return HttpResponse('<h1>This is about me!.</h1>')

def podium(request):
    return HttpResponse('<h1>podiuuuuuuuuu<h1>')

def location(request):
    return HttpResponse('<h1>location<h1>')

def index(request):

    num_books = 15
    num_instances = 20
    num_instances_available = 5
    num_authors = 10

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    return render(request, 'html/test.html', context=context)