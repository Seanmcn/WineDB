from django.db import models


class History(models.Model):
    wine_count = models.IntegerField()
    url = models.URLField()
    date = models.DateTimeField('date harvested')

    def __str__(self):
        return self.url


class Wines(models.Model):
    name = models.CharField(max_length=300)
    color = models.CharField(max_length=50)
    grape = models.CharField(max_length=150)
    location = models.CharField(max_length=300)
    price = models.IntegerField()
    rating = models.IntegerField()
    description = models.TextField()
    mix = models.CharField(max_length=300)
    date = models.DateTimeField('date published')
    harvestedFrom = models.ForeignKey(History)

    def __str__(self):
        return self.name
