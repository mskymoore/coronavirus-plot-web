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

confirmed = repo.get_contents("csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
deaths = repo.get_contents("csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
recovered = repo.get_contents("csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")

case_status_type_names = ['confirmed', 'deaths', 'recovered']

csv_github_files = [confirmed, deaths, recovered]

csv_urls = [github_file.download_url for github_file in csv_github_files]

csv_files = [get_file(csv_url) for csv_url in csv_urls]

case_files = {}

for case_status_type_name, csv_file in zip(case_status_type_names,csv_files):
    case_files[case_status_type_name] = csv_file