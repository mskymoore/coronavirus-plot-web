import csv, requests, pickle
from .models import CaseStatusType, Location, HistoricEntry
from hashlib import sha256

from github import Github


province_key = 'Province/State'
country_key = 'Country/Region'


def get_file(csv_url):
    return csv.DictReader(requests.get(csv_url).iter_lines(decode_unicode=True))


g = Github("34a2755ef5ef33b83bf7bcf4614a27f6287d5589")

repo = g.get_repo("CSSEGISandData/COVID-19")
confirmed = repo.get_contents("csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
death = repo.get_contents("csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
recovered = repo.get_contents("csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")

list1=[1,2,3]
list2=[4,5,6]
for item in zip(list1,list2):
    print(item)
exit()
data_file = get_file(confirmed.download_url)
print('\n\n',data_file.fieldnames, '\n\n')
for line in data_file:
    print(line)
    input()
exit()

def generate_count_series(row):
    return pickle.dumps([int(row[num]) for num in row if (row[num].isnumeric() and int(row[num]) > 0)])


def update_table(csv_url_key, series_type):

    update_file = get_file(csv_urls[csv_url_key])
    locs = { create_hash(loc.friendly_name): loc for loc in Location.objects.all() }

    casetypes = svc.get_casetypes
    for row in update_file:
        province = row[province_key]
        region = row[country_key]
        hash_value = create_hash(province + ' - ' + region if province_state is not None  else region
        
        #last_entry = HistoricEntry.objects.filter(location_id=location.id).order_by('date').last()

        num_db_entries = len(HistoricEntry.objects.filter(location_id=location.id))
        cur = locs[hash_value]
        
        # [(a,2), (b,3), (c,4)] # in db
        # [(z,0), (a,2), (b,3), (c,4), (d,5)] # in row
        #

        for i, item in enumerate(row[]):
            if item.isnumeric() and int(item) > 0:
                    first_entry_index = i + 1
                    break
        

        start = (e-)
        for item in row[target:]    

def create_hash(value):
    return str(sha256(value.encode()))


def get_selection_string(row):
    selection_string = None
    if row[country_key] != '' and row[province_key].count(',') == 0:
        if row[province_key] == '':
            selection_string = SelectionString(selection_string=row[country_key])
        else:
            selection_string = SelectionString(selection_string=row[province_key] + ' - ' + row[country_key])
    return selection_string


def generate_location(selection_string, row):
    location = Location(
                    selection_string=selection_string,
                    province_state=row[province_key],
                    region_country=row[country_key]
                )
    return location


data_file = get_file(confirmed_cases_csv_url)

date_series = DateSeries(date_series=pickle.dumps(data_file.fieldnames[4:])).save()



for row in data_file:
    selection_string = get_selection_string(row)
    if selection_string is not None:
        selection_string.save()
        location = generate_location(selection_string, row)
        location.save()


for csv_url_key in csv_urls:
        update_table(csv_url_key, csv_url_key)