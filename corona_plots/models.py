from django.db import models
from django.utils import timezone
from hashlib import sha256
import pickle

# Create your models here.

def create_friendly_name(province, region):
    return str(province) + ' - ' + str(region) if str(province) is not '' else str(region)


def create_hash(friendly_name):
    return sha256(friendly_name.encode()).hexdigest()


class Location(models.Model):
    province_state = models.CharField(max_length=100, default='')
    region_country = models.CharField(max_length=100, default='')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=100)
    friendly_hash = models.CharField(max_length=100)
    def __str__(self):
        return self.friendly_name


class HistoricEntry(models.Model):
    date = models.DateField()
    count = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    case_status_type_id = models.CharField(max_length=25)
    def __str__(self):
       return str(self.date) + ':' + str(self.count)