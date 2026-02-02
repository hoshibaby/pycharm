from django.urls import path
from . import views

app_name = 'dataprocess'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('charts/', views.charts, name='charts'),
    path('map/', views.map_view, name='map'),
    path('wordclouds/', views.wordclouds, name='wordclouds'),
    path('cnn/', views.image_pred, name='cnn')
]