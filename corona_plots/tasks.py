import csv, requests
from .models import Location, HistoricEntry, create_friendly_name, create_hash
from .coronaVars import province_key, country_key, csv_urls, get_file
from .coronaVars import case_status_type_names, lat_key, long_key
from celery import shared_task
from celery.signals import worker_ready
from datetime import datetime as dt
from hashlib import sha256


# csv_file: csv.DictReader
# case_status_type: string, one of ['confirmed', 'deaths', 'recovered']
def update_database(csv_file, case_status_type_id):

    locs = { loc.friendly_hash: loc for loc in Location.objects.all() }

    for row in csv_file:

        province = row[province_key]
        region = row[country_key]
        lat = row[lat_key]
        lon = row[long_key]

        friendly_name = create_friendly_name(province, region)
        friendly_hash = create_hash(friendly_name)
        
        if friendly_hash not in locs:
            location = Location(
                province_state = province,
                region_country = region,
                latitude = lat,
                longitude = lon,
                friendly_name = friendly_name,
                friendly_hash = friendly_hash
            )
            location.save()
        else:
            location = locs[friendly_hash]

        locations_entries = HistoricEntry.objects.filter(location_id=location, case_status_type_id=case_status_type_id) 
        num_historic_db_entries = len(locations_entries)
        
        list_row = [ item for item in row.items() ][4:]

        if num_historic_db_entries == len(list_row):
            # no new entries, nothing to do
            print('no updates for', case_status_type_id)
            break 

        for entry in list_row[num_historic_db_entries:]:
            HistoricEntry(
                date = dt.strptime(entry[0], '%m/%d/%y').strftime('%Y-%m-%d'),
                location = location,
                count = int(entry[1]),
                case_status_type_id = case_status_type_id
            ).save()
            print('new {status_type} historical entry {num} for {date} {location}'.format(
                status_type=case_status_type_id,
                num=entry[1],
                date=entry[0],
                location=location.friendly_name))
            

@shared_task
def do_data_update():
    csv_files = [get_file(csv_url) for csv_url in csv_urls]

    for case_status_type_name, csv_file in zip(case_status_type_names, csv_files):
        update_database(csv_file, case_status_type_name)

@worker_ready.connect
def update_data(sender=None, conf=None, **kwargs):
    do_data_update()