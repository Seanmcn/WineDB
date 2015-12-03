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

    eyes = models.TextField()
    nose = models.TextField()
    mouth = models.TextField()
    overall = models.TextField()
    producer = models.TextField()

    region = models.CharField(max_length=150)
    sub_region = models.CharField(max_length=150)
    variety = models.CharField(max_length=150)
    vintage = models.CharField(max_length=150)

    price = models.IntegerField()
    description = models.TextField()

    harvest_data = models.TextField()
    harvested_from = models.ForeignKey(History)
    harvested_date = models.DateTimeField('date harvested')

    def __str__(self):
        return self.name
