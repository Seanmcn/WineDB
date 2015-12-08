from django.db import models


class History(models.Model):
    wine_count = models.IntegerField()
    url = models.URLField()
    date = models.DateTimeField('date harvested')

    def __str__(self):
        return self.url


class Wines(models.Model):
    name = models.CharField(max_length=300)
    color = models.CharField(max_length=50, default='N/A')

    eyes = models.TextField()
    nose = models.TextField()
    mouth = models.TextField()
    overall = models.TextField()
    producer = models.TextField()

    abv = models.CharField(max_length=100, default='N/A')
    region = models.CharField(max_length=150, default='N/A')
    sub_region = models.CharField(max_length=150, default='N/A')
    variety = models.CharField(max_length=150, default='N/A')
    vintage = models.CharField(max_length=150, default='N/A')
    tags = models.CharField(max_length=300, default='')

    price = models.IntegerField(default=0)
    description = models.TextField()

    harvest_data = models.TextField()
    harvested_from = models.ForeignKey(History)
    harvested_date = models.DateTimeField('date harvested')

    def __str__(self):
        return self.name
