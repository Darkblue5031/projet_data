from django.shortcuts import render
from django.http import HttpResponse

def about(request):
    return HttpResponse('<h1>This is about me!.</h1>')

def podium(request):
    return HttpResponse('<h1>podiuuuuuuuuu<h1>')

def location(request):
    return HttpResponse('<h1>location<h1>')

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = 15
    num_instances = 20

    # Available books (status = 'a')
    num_instances_available = 5

    # The 'all()' is implied by default.
    num_authors = 10

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)