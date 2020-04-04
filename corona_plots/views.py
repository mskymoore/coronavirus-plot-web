from django.shortcuts import render
from .coronaVars import case_status_type_names
from .models import Location, HistoricEntry
import plotly.offline as po
import plotly.express as px


# TODO: generate graphs when updating database and store in database or in filesystem,
# retrieve them when requested instead of generating them since data only updates once a day
# also use javascript to place a spinner, request the images, then replace the spinner with the image
# after the image is recieved.
def generate_graph_div(series_type, location):
        entries = HistoricEntry.objects.filter(location=location,case_status_type_id=series_type).order_by('date')
        x_axis_cases = []
        y_axis_cases = []
        for entry in entries:
            x_axis_cases.append(str(entry.date))
            y_axis_cases.append(int(entry.count))

        y_axis_increase = [y_axis_cases[0]]
        for i in range(len(entries))[1:]:
            y_axis_increase.append(y_axis_cases[i] - y_axis_cases[i-1])

        y_axis_increase_percent = [0]
        for i in range(len(entries))[1:]:
            if y_axis_cases[i-1] == 0:
                divisor = 100
            else:
                divisor = y_axis_cases[i-1]
            y_axis_increase_percent.append(((y_axis_cases[i] - y_axis_cases[i-1])/divisor)*100)


        fig_line = px.line(x=x_axis_cases, y=y_axis_cases, title=f'{series_type} cases', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} cases'})
        line_graph_div = po.plot(fig_line, auto_open=False, output_type="div", include_plotlyjs=False)
        
        fig_bar = px.bar(x=x_axis_cases, y=y_axis_increase, title=f'{series_type} increase', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} increase'})
        bar_graph_div = po.plot(fig_bar, auto_open=False, output_type="div", include_plotlyjs=False)

        fig_bar_perc = px.bar(x=x_axis_cases, y=y_axis_increase_percent, title=f'{series_type} percent increase', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} percent increase'})
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

    context = {
        'graphs': [ generate_graph_div(series_type, location) for series_type in case_status_type_names ],
        'title': location,
        'locations': Location.objects.all().order_by('friendly_name')
    }
    
    return render(request, 'corona_plots/home.html', context)


def plot(request):
    location = request.GET['location']
    location = Location.objects.filter(friendly_name=location).first()
    