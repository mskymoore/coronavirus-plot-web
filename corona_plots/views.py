from django.shortcuts import render
from .coronaVars import case_status_type_names
from .models import Location, HistoricEntry
import plotly.offline as po
import plotly.express as px


# Create your views here.
def home(request):
    context = {'locations': Location.objects.all().order_by('friendly_name'),
                'title': 'Choose a Location'}
    return render(request, 'corona_plots/home.html', context)


def plots(request):
    location = request.GET['location']
    location = Location.objects.filter(friendly_name=location).first()

    def generate_graph_div(series_type, selection_string):
        entries = HistoricEntry.objects.filter(location=location,case_status_type_id=series_type).order_by('date')
        x_axis = []
        y_axis = []
        for entry in entries:
            x_axis.append(str(entry.date))
            y_axis.append(int(entry.count))


        fig = px.line(x=x_axis, y=y_axis, title=f'{series_type} cases', labels={'x': 'date', 'y':f'{series_type} cases'})
        graph_div = po.plot(fig, auto_open = False, output_type="div")
        
        return graph_div
        

    context = {
        'graphs': [ generate_graph_div(series_type, location) for series_type in case_status_type_names ],
        'title': location,
        'locations': Location.objects.all().order_by('friendly_name')
    }
    
    return render(request, 'corona_plots/home.html', context)
