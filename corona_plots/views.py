from django.shortcuts import render

lil_key = 'provinces'
big_key = 'country'

# Create your views here.
def home(request):
    context = {
        'location_keys': {'lil': lil_key, 'big': big_key},
        'locations': ['locationa', 'locationb', 'locationc'],
        'location_dict': {
            'locationa': {
                lil_key : 'aprovince',
                big_key : 'acountry'
            },
            'locationb': {
                lil_key : 'bprovince',
                big_key : 'bcountry'
            },
            'locationc': {
                lil_key : 'cprovince',
                big_key : 'ccountry'
            }
        }
    }
    return render(request, 'corona_plots/home.html', context)


def plots(request):
    context = {
        'plots': ['plot1.img', 'plot2.img']
    }
    return render(request, 'corona_plots/plots.html', context)