from django.db import models

class Data(models.Model):
    Age = models.IntegerField()
    Gender = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Gender} - {self.Age}"

    class Meta:
        db_table = 'data'