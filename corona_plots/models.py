from django.db import models
from django.utils import timezone
from hashlib import sha256
import pickle

# Create your models here.

class CaseStatusType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return str(self.name)

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    province_state = models.CharField(max_length=100, default='')
    region_country = models.CharField(max_length=100, default='')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    friendly_name =  str(province_state) + ' - ' + str(region_country) if province_state is not None  else str(region_country)
    friendly_hash = models.IntegerField(default=str(sha256(friendly_name.encode())))
    def __str__(self):
        return self.friendly_name
    
class HistoricEntry(models.Model):
    date = models.DateField()
    count = models.IntegerField(default=0)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    case_status_type_id = models.ForeignKey(CaseStatusType, on_delete=models.DO_NOTHING)
    def __str__(self):
       return str(self.date) + ':' + str(self.count)