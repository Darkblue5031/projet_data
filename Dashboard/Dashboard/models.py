from django.db import models
import django.db.models as mod

class Data(models.Model):
    Age = models.IntegerField()
    Gender = models.CharField(max_length=100)
    Marital_Status = models.CharField(max_length=100)
    Occupation = models.CharField(max_length=100)
    Monthly_Income = models.CharField(max_length=100)
    Educational_Qualifications = models.CharField(max_length=100)
    Family_Size = models.IntegerField()
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Postal_Code = models.IntegerField()
    Output = models.BooleanField()
    Feedback = models.CharField(max_length=100)
    M = models.BooleanField()

    @classmethod
    def average(cls, column):
        return cls.objects.aggregate(avg=mod.Avg(column))['avg']

    @classmethod
    def sum(cls, column):
        return cls.objects.aggregate(sum=mod.Sum(column))['sum']

    @classmethod
    def count(cls, column):
        return cls.objects.aggregate(count=mod.Count(column))['count']

    @classmethod
    def min(cls, column):
        return cls.objects.aggregate(min=mod.Min(column))['min']

    @classmethod
    def max(cls, column):
        return cls.objects.aggregate(max=mod.Max(column))['max']

    def __str__(self):
        return f"{self.Gender} - {self.Age}"

    class Meta:
        db_table = 'data'