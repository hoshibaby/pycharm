from django.shortcuts import render

from dataprocess.datapro import *


# Create your views here.
def dashboard(request):
    return render(request, 'dataprocess/dashboard.html')

def statistics(request):
    return render(request, 'dataprocess/statistics.html')

def charts(request):
    df = chart_draw()
    data = df.values
    return render(request, 'dataprocess/charts.html', {'data' : data})

def map_view(request):
    map_draw()
    return render(request, 'dataprocess/map.html')

def wordclouds(request):
    return render(request, 'dataprocess/wordclouds.html')