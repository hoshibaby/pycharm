import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from konlpy.tag import *
from wordcloud import WordCloud
from folium import plugins

from mysite.settings import BASE_DIR


def chart_draw():
    data = pd.read_excel('static/files/04_data1.xlsx')
    good_df = data[['area', '2020_good']]
    print(good_df)
    plt.figure(figsize=(10, 8))
    good_df.plot(kind='bar')
    plt.savefig('static/images/bar_chart.png')
    return good_df

def map_draw():
    df = pd.read_csv('static/files/CCTV_20190917.csv')
    print(df.head())
    df1 = df.loc[df['카메라대수']>=1,:]
    print(df1.head())
    popups = df1['소재지도로명주소'].to_list()
    print(popups)
    lat_avg = np.array(df1['위도'].to_list()).mean()
    lon_avg = np.array(df1['경도'].to_list()).mean()
    m = folium.Map(location=[lat_avg, lon_avg], zoom_start=12)
    data = np.array([df1['위도'].to_list(), df1['경도'].to_list()]).T
    plugins.MarkerCluster(data, popups=popups).add_to(m)
    m.save('templates/dataprocess/map01.html')

def wordcloud_draw():
    df = pd.read_csv('static/files/2015.csv')