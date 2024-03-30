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
    genders = Data.objects.values_list("Gender", flat=True)
    ages = Data.objects.values_list("Age", flat=True)
    maritals_status = Data.objects.values_list("Marital_Status", flat=True)
    occupations = Data.objects.values_list("Occupation", flat=True)
    Monthly_income = Data.objects.values_list("Monthly_Income", flat=True)
    Educational_qualification = Data.objects.values_list("Educational_Qualifications", flat=True)
    latitudes = Data.objects.values_list("Latitude", flat=True)
    longitudes = Data.objects.values_list("Longitude", flat=True)
    postal_codes = Data.objects.values_list("Postal_Code", flat=True)
    feedbacks = Data.objects.values_list("Feedback", flat=True)
    families_size = Data.objects.values_list("Family_Size", flat=True)

    Age_average = Data.Average(Data.Age.field.name)
    Age_min = Data.Min(Data.Age.field.name)
    Age_median = Data.Median(Data.objects.values_list("Age", flat=True))

    ratio_male = Data.Ratio_conditional("Gender", "Male")
    family_3 = Data.Ratio_conditional("Latitude", 3.0, "sup")

    context = {
        'genders': genders,
        'ages': ages,
        'maritals_status': maritals_status,
        'occupations': occupations,
        'monthly_income': Monthly_income,
        'educational_qualification': Educational_qualification,
        'families_size': families_size,
        'latitudes': latitudes,
        'longitudes': longitudes,
        'pin_codes': postal_codes,
        'feedbacks': feedbacks,
        'family_3': family_3,
    }
    print(f"coucou{family_3}")
    print(f"avearaaaaaaaaaaaaag{Age_average}")

    return render(request, 'html/test.html', context=context)
