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
    genders = (Data.objects.values_list("Gender", flat=True))
    ages = (Data.objects.values_list("Age", flat=True))
    maritals_status = (Data.objects.values_list("Marital_Status", flat=True))

    Age_average = Data.average(Data.Age.field.name)
    Age_min = Data.min(Data.Age.field.name)
    Age_median = Data.median(Data.objects.values_list("Age", flat=True))

    context = {
        'genders': genders,
        'ages': ages,
        'maritals_status': maritals_status,
        'Age_average': Age_average,
        'Age_min': Age_min,
        'Age_median': Age_median,
    }
    return render(request, 'html/test.html', context=context)