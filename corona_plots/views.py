from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        'this_key': 'is a variable accssible in the template'
    }
    return render(request, 'corona_plots/home.html', context)