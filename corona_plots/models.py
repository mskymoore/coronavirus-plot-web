from django.db import models
from django.utils import timezone
import pickle

# Create your models here.

class SelectionString(models.Model):
    selection_string = models.CharField(primary_key=True, max_length=100)
    def __str__(self):
        return self.selection_string

class DateSeries(models.Model):
    date_retrieved = models.DateTimeField(primary_key=True, default=timezone.now)
    date_series = models.BinaryField(max_length=None, default=[])
    def __str__(self):
        return str(pickle.loads(self.date_series))

class Location(models.Model):
    selection_string = models.OneToOneField(SelectionString, on_delete=models.CASCADE)
    province_state = models.CharField(max_length=100, default='')
    region_country = models.CharField(max_length=100, default='')
    def __str__(self):
       return str(self.selection_string)

class SeriesType(models.Model):
    selection_string = models.ForeignKey(SelectionString, on_delete=models.CASCADE)
    series_type = models.CharField(max_length=100)
    def __str__(self):
        return str(self.series_type)

class CountSeries(models.Model):
    selection_string = models.ForeignKey(SelectionString, on_delete=models.CASCADE)
    series_type = models.OneToOneField(SeriesType, on_delete=models.CASCADE)
    count_series = models.BinaryField(max_length=None, default=[])
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.selection_string) + ' ' + str(self.series_type) + '\n' + str(pickle.loads(self.count_series))


