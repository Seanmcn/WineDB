from django.db import models

# Create your models here.
class History(models.Model):
    wine_count = models.IntegerField()
    url = models.URLField()
    date = models.DateTimeField('date harvested')


class Wines(models.Model):
    name = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    price = models.IntegerField()
    rating = models.IntegerField()
    description = models.TextField()
    simple_type = models.CharField(max_length=50)
    advanced_type = models.CharField(max_length=150)
    mix = models.CharField(max_length=300)
    date = models.DateTimeField('date published')
    harvestedFrom = models.ForeignKey(History)