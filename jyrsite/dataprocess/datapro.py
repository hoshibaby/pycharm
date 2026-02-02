import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from konlpy.tag import *
from wordcloud import WordCloud
from folium import plugins
import os
import json
import folium
from django.conf import settings

from jyrsite.settings import BASE_DIR

def statistics():
    base_path = os.path.join(settings.BASE_DIR, 'static', 'files')

    summary_path = os.path.join(base_path, 'happiness_summary.csv')
    corr_path = os.path.join(base_path, 'happiness_correlation.csv')

    summary_df = pd.read_csv(summary_path)
    corr_df = pd.read_csv(corr_path, header=None)

    avg_happiness = float(summary_df.loc[0, '값'])
    corr_happy_health = float(summary_df.loc[1, '값'])
    corr_happy_financial = float(summary_df.loc[2, '값'])

    corr_matrix = corr_df.values.tolist()

    return [
        avg_happiness,
        corr_happy_health,
        corr_happy_financial,
        corr_matrix
    ]


def chart_draw():
    return 'images/bar_chart.png'

def map_draw():
    # 1) 엑셀 읽기 (xlsx는 read_excel)
    df = pd.read_excel('static/files/행정구역_시군구_별__성별_인구수.xlsx')

    # 2) 시도별 "소계"만 남기고 sido, total만 뽑기
    sido_all = df.loc[df['gugun'] == '소계', ['sido', 'total']].copy()

    # 3) GeoJSON 로드
    with open('static/files/ctprvn.json', encoding='utf-8') as f:
        sido_geo = json.load(f)

    # 4) 지도 생성
    m = folium.Map(location=[36.5, 127.8], zoom_start=7)

    # 5) Choropleth 색칠
    folium.Choropleth(
        geo_data=sido_geo,
        data=sido_all,
        columns=['sido', 'total'],
        key_on='properties.CTP_KOR_NM',
        fill_color='RdYlGn',
        fill_opacity=0.6,
        line_opacity=0.2,
        legend_name='시도별 총 인구수'
    ).add_to(m)

    # 6) 저장 경로 (Django에서 iframe으로 쓰기 좋게 static에 저장)
    out_dir = os.path.join('static', 'maps')
    os.makedirs(out_dir, exist_ok=True)

    out_path = "static/maps/map.html"
    m.save(out_path)

    return out_path

def wordcloud_draw():
    df = pd.read_csv('static/files/2015.csv')