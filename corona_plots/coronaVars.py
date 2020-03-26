import csv, requests
from github import Github

def get_file(csv_url):
    return csv.DictReader(requests.get(csv_url).iter_lines(decode_unicode=True))

province_key = 'Province/State'
country_key = 'Country/Region'
lat_key = 'Lat'
long_key = 'Long'

g = Github("34a2755ef5ef33b83bf7bcf4614a27f6287d5589")
repo = g.get_repo("CSSEGISandData/COVID-19")

confirmed_path = "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_path = "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
confirmed = repo.get_contents(confirmed_path)
deaths = repo.get_contents(deaths_path)


case_status_type_names = ['confirmed', 'deaths']

csv_github_files = [confirmed, deaths]

csv_urls = [github_file.download_url for github_file in csv_github_files]