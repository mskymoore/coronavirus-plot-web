import csv, requests
from .models import CaseStatusType, Location, HistoricEntry, create_friendly_name, create_hash
from .coronaVars import province_key, country_key, case_files, lat_key, long_key
from datetime import datetime as dt
from hashlib import sha256



# [(a,2), (b,3), (c,4)] # in db
# [(z,0), (a,2), (b,3), (c,4), (d,5)] # in row
#

# csv_file: csv.DictReader
# case_status_type: string, one of ['confirmed', 'deaths', 'recovered']
def update_table(csv_file, case_status_type_name):

    case_status_type_name_id_dict = { cst.name: cst for cst in CaseStatusType.objects.all() }
    locs = { loc.friendly_hash: loc for loc in Location.objects.all() }

    if case_status_type_name not in case_status_type_name_id_dict:
        case_status_type = CaseStatusType(name=case_status_type_name)
        case_status_type.save()
        #case_status_type_id = case_status_type.id
    else:
        case_status_type = case_status_type_name_id_dict[case_status_type_name]

    for row in csv_file:

        province = row[province_key]
        region = row[country_key]
        lat = row[lat_key]
        lon = row[long_key]

        hash_value = create_hash(
                        create_friendly_name(
                            province,
                            region
                        )
                     )
        
        if hash_value not in locs:
            location = Location(
                province_state = province,
                region_country = region,
                latitude = lat,
                longitude = lon
            )
            location.save()
        else:
            location = locs[hash_value]
        
        num_historic_db_entries = len(HistoricEntry.objects.filter(location_id=location))
        
        list_row = [ item for item in row.items() ][4:]

        for i, entry in enumerate(list_row):
            if int(entry[1]) > 0 :
                first_nonzero_row_entry_index = i
                break

        first_new_entry_index = first_nonzero_row_entry_index + num_historic_db_entries
        
        for entry in list_row[first_new_entry_index:]:
            HistoricEntry(
                date = dt.strptime(entry[0], '%m/%d/%y').strftime('%Y-%m-%d'),
                location_id = location.id,
                count = int(entry[1]),
                case_status_type_id = case_status_type
            ).save()


for case_file_type in case_files:
        update_table(case_files[case_file_type], case_file_type)