from django.db import models
from django.utils import timezone

# Create your models here.

class SelectionString(models.Model):
    selection_string = models.CharField(primary_key=True, max_length=100)

class DateSeries(models.Model):
    date_retrieved = models.DateTimeField(primary_key=True, default=timezone.now)
    date_series = models.BinaryField(max_length=None, default=[])

class Location(models.Model):
    selection_string = models.OneToOneField(SelectionString, on_delete=models.CASCADE)
    province_state = models.CharField(max_length=100, default='')
    region_country = models.CharField(max_length=100, default='')

class CountSeries(models.Model):
    selection_string = models.ForeignKey(SelectionString, on_delete=models.CASCADE)
    series_type = models.CharField(max_length=100)
    count_series = models.BinaryField(max_length=None, default=[])
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

