from django.db import models


class History(models.Model):
    wine_count = models.IntegerField()
    url = models.URLField()
    date = models.DateTimeField('date harvested')

    def __str__(self):
        return self.url


COLOR_CHOICES = (
    ('N/A', 'N/A'),
    ('Red', 'Red'),
    ('White', 'White'),
    ('Orange', 'Orange'),
    ('Rosé', 'Rosé'),
)


# First, define the Manager subclass.
class WineManager(models.Manager):
    def get_queryset(self):
        return super(WineManager, self).get_queryset().filter(deleted=False)


class Wine(models.Model):
    name = models.CharField(max_length=300)
    color = models.CharField(max_length=50, default='N/A', choices=COLOR_CHOICES)

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

    price = models.CharField(max_length=150, default=0)
    description = models.TextField()

    harvest_data = models.TextField()
    harvested_from = models.ForeignKey(History)
    harvested_date = models.DateTimeField('date harvested')

    is_wine = models.BooleanField(default=True)
    was_modified = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    # wines = models.Manager()
    objects = WineManager()
    wines = models.Manager()

    def __str__(self):
        return self.name

    # @staticmethod
    def get_all(self):
        return Wine.wines.all(self).filter(is_wine=True, deleted=False)

    def save(self, *args, **kwargs):
        self.was_modified = True
        super(Wine, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted = True
        super(Wine, self).save(*args, **kwargs)

    def harvest_delete(self, *args, **kwargs):
        super(Wine, self).delete(*args, **kwargs)

    def harvest_save(self, *args, **kwargs):
        self.was_modified = False
        super(Wine, self).save(*args, **kwargs)
