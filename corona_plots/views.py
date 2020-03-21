from django.shortcuts import render
from . import models
import pickle
import plotly.offline as po
import plotly.express as px


# Create your views here.
def home(request):
    context = {'locations': models.SelectionString.objects.order_by('selection_string')}
    return render(request, 'corona_plots/home.html', context)


def plots(request):
    series_types = ['confirmed', 'death', 'recovered']
    location = request.GET['location']
    def generate_graph_div(series_type, selection_string):
        y_axis = models.SeriesType.objects.filter(
             series_type=series_type,
             selection_string=selection_string
             ).first()
        y_axis = pickle.loads(models.CountSeries.objects.filter(series_type=y_axis).first().count_series)
        x_axis = pickle.loads(models.DateSeries.objects.all().first().date_series)[-len(y_axis):]
        x_axis = [ x_axis[i] for i in range(len(y_axis)) ]


        if len(x_axis) == len(y_axis) and len(y_axis) > 0:
            # fig is plotly figure object and graph_div the html code for displaying the graph
            fig = px.line(x=x_axis, y=y_axis, title=f'{series_type} cases {selection_string}', labels={'x': 'date', 'y':f'{series_type} cases'})
            graph_div = po.plot(fig, auto_open = False, output_type="div")
        
            return graph_div
        return ''

    context = {
        'graphs': [ generate_graph_div(series_type, location) for series_type in series_types ]
    }
    
    return render(request, 'corona_plots/plots.html', context)
