from django.shortcuts import render
from .coronaVars import case_status_type_names
from .models import Location, HistoricEntry
import plotly.offline as po
import plotly.express as px


# TODO: generate graphs when updating database and store in database or in filesystem,
# retrieve them when requested instead of generating them since data only updates once a day
# also use javascript to place a spinner, request the images, then replace the spinner with the image
# after the image is recieved.

def generate_percent_increase_series(y_axis_cases):
    
    y_axis_percent_increase = [0]
    for i in range(len(y_axis_cases))[1:]:
        if y_axis_cases[i-1] == 0:
            divisor = 100
        else:
            divisor = y_axis_cases[i-1]
        y_axis_percent_increase.append(((y_axis_cases[i] - y_axis_cases[i-1])/divisor)*100)
    
    return y_axis_percent_increase


def generate_series(series_type, location):
    entries = HistoricEntry.objects.filter(location=location,case_status_type_id=series_type).order_by('date')
    x_axis_cases = []
    y_axis_cases = []
    for entry in entries:
        x_axis_cases.append(str(entry.date))
        y_axis_cases.append(int(entry.count))

    y_axis_increase = [y_axis_cases[0]]
    for i in range(len(entries))[1:]:
        y_axis_increase.append(y_axis_cases[i] - y_axis_cases[i-1])
    
    y_axis_percent_increase = generate_percent_increase_series(y_axis_cases)

    
    return {
        'x_axis' : x_axis_cases,
        'cases' : y_axis_cases,
        'increase' : y_axis_increase,
        'percent_increase' : y_axis_percent_increase
    }


def generate_graph_div(series, series_type):
    x_axis_cases = series['x_axis']
    y_axis_cases = series['cases']
    y_axis_increase = series['increase']
    y_axis_percent_increase = series['percent_increase']

    fig_line = px.line(x=x_axis_cases, y=y_axis_cases, title=f'{series_type} cases', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} cases'})
    line_graph_div = po.plot(fig_line, auto_open=False, output_type="div", include_plotlyjs=False)
        
    fig_bar = px.bar(x=x_axis_cases, y=y_axis_increase, title=f'{series_type} increase', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} increase'})
    bar_graph_div = po.plot(fig_bar, auto_open=False, output_type="div", include_plotlyjs=False)

    fig_bar_perc = px.bar(x=x_axis_cases, y=y_axis_percent_increase, title=f'{series_type} percent increase', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} percent increase'})
    bar_perc_graph_div = po.plot(fig_bar_perc, auto_open=False, output_type="div", include_plotlyjs=False)

    return line_graph_div + bar_perc_graph_div + bar_graph_div


# Create your views here.
def home(request):
    context = {'locations': Location.objects.all().order_by('friendly_name'),
                'title': 'Choose a Location'}
    return render(request, 'corona_plots/home.html', context)


def plots(request):
    location = request.GET['location']
    location = Location.objects.filter(friendly_name=location).first()

    if location.county == '':
        context = {
            'graphs': [ generate_graph_div(generate_series(series_type, location), series_type) for series_type in case_status_type_names ],
            'title': location,
            'locations': Location.objects.all().order_by('friendly_name')
        }
    else:
        context = {
            'graphs': [ generate_graph_div(generate_series(series_type, location), series_type) for series_type in case_status_type_names[:2] ],
            'title': location,
            'locations': Location.objects.all().order_by('friendly_name')
        }
    
    return render(request, 'corona_plots/home.html', context)


def get_states_by_region(request):
    pass

def get_counties_by_state(request):
    pass

def get_regions(request):
    pass


def plots2(request):
    location = request.GET['location']
    locations = Location.objects.filter(province_state=location).all()
    location_series = {}
    
    for sublocation in locations:
        location_series[sublocation.friendly_hash] = { series_type : generate_series(series_type, sublocation) for series_type in case_status_type_names[:2] }
    
    location_sum_series = {}

    for series_type in case_status_type_names[:2]:
        x_axis = location_series[next(iter(location_series))][series_type]['x_axis']
        y_axis_cases = [ 0 for i in x_axis ]
        y_axis_increase = y_axis_cases.copy()

        for sublocation in location_series:

            for i, count in enumerate(location_series[sublocation][series_type]['cases']):
                y_axis_cases[i] = y_axis_cases[i] + count

            for i, count in enumerate(location_series[sublocation][series_type]['increase']):
                y_axis_increase[i] = y_axis_increase[i] + count
            
        y_axis_percent_increase = generate_percent_increase_series(y_axis_cases)
            

        location_sum_series[series_type] = {
            'x_axis' : x_axis,
            'cases' : y_axis_cases,
            'increase' : y_axis_increase,
            'percent_increase' : y_axis_percent_increase
        }

    context = context = {
            'graphs': [ generate_graph_div(location_sum_series[series_type], series_type) for series_type in location_sum_series ],
            'title': location,
            'locations': Location.objects.all().order_by('friendly_name')
        }
    return render(request, 'corona_plots/home.html', context)

    



        


def plot(request):
    location = request.GET['location']
    location = Location.objects.filter(friendly_name=location).first()
    