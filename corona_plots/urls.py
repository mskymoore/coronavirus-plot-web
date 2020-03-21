from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='corona-plots-home'),
    path('plots/', views.plots, name='corona-plots-plots')
]