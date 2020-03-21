from .models import DateSeries, Location, SelectionString, CountSeries, SeriesType
import csv, requests, pickle


confirmed_cases_csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
death_csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
recovered_cases_csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"

csv_urls = {'confirmed': confirmed_cases_csv_url, 'death': death_csv_url, 'recovered': recovered_cases_csv_url}

province_key = 'Province/State'
country_key = 'Country/Region'



def get_file(csv_url):
    return csv.DictReader(requests.get(csv_url).iter_lines(decode_unicode=True))


def generate_count_series(row):
    return pickle.dumps([int(row[num]) for num in row if (row[num].isnumeric() and int(row[num]) > 0)])


def update_table(csv_url_key, series_type):
    update_file = get_file(csv_urls[csv_url_key])
    for row in update_file:
        selection_string = get_selection_string(row)
        selection_string = SelectionString.objects.filter(selection_string=selection_string).first()
        if selection_string is not None:
            series_type = SeriesType(
                selection_string=selection_string,
                series_type=series_type
            )
            series_type.save()
            count_series = CountSeries(
                selection_string=selection_string,
                series_type=series_type,
                count_series=generate_count_series(row),
                location=Location.objects.filter(selection_string=selection_string).first()
            )
            count_series.save()


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