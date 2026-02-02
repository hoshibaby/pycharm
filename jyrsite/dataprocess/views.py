from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from dataprocess.datapro import (statistics as calc_statistics, chart_draw, map_draw)

from dataprocess.datapro import *
from .imageTest import image_test, image_one_test

# Create your views here.
def dashboard(request):
    return render(request, 'dataprocess/dashboard.html')

def statistics_view(request):
    corr_data = calc_statistics()
    return render(request, 'dataprocess/statistics.html', {
          'avg_happiness': corr_data[0],
          'corr_happy_health': corr_data[1],
          'corr_happy_financial': corr_data[2],
          'corr_matrix': corr_data[3],
    })


def charts(request):
    chart_path = chart_draw()   # 'images/bar_chart.png'
    return render(request, 'dataprocess/charts.html', {
        'chart_path': chart_path
    })

def map_view(request):
    map_draw()
    return render(request, 'dataprocess/map.html')

def wordclouds(request):
    return render(request, 'dataprocess/wordclouds.html')

#-------------------------------------------
#model 추가 중
def image_one_pred(request):
    if request.method=='POST' and request.FILES['image']:
        image = request.FILES['image']
        fs=FileSystemStorage(location='static/images/uploads')
        filename = fs.save(image.name, image)
        filepath = fs.path(filename)

    context=image_one_test(filepath)
    return render(request,'dataprocess/upload.html',
                  {'content':context})