from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from constants import TIME_FORMAT, SERVICES_LIST, STATUS
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re

app = Flask(__name__)

@app.route('/faq', methods=['GET', 'POST'])
def faq():
    return render_template('faq.html', alerttype='success', url=url)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['tripData']
      analyticsObj = basic_analytics(f)
      return render_template('analytics.html', data=analyticsObj)


def basic_analytics(file):
    df = pd.read_csv(file)
    df.rename(columns={'Product Type':'Service','Fare Amount':'Cost','Begin Trip Time':'BeginTimestamp',
                       'Dropoff Time':'EndTimestamp','Request Time':'RequestTimestamp','Distance (miles)':'Distance'}, inplace=True)
    df["BeginTimestamp"] = df["BeginTimestamp"].str.replace(" UTC", "")
    df["EndTimestamp"] = df["EndTimestamp"].str.replace(" UTC", "")
    df["RequestTimestamp"] = df["RequestTimestamp"].str.replace(" UTC", "")
    df.BeginTimestamp = pd.to_datetime(df.BeginTimestamp, format=TIME_FORMAT)
    df.EndTimestamp = pd.to_datetime(df.EndTimestamp, format=TIME_FORMAT)
    df.RequestTimestamp = pd.to_datetime(df.RequestTimestamp, format=TIME_FORMAT)
    df['Year'] = df.apply(lambda x: x.BeginTimestamp.year,axis=1)
    df['TripTime'] = df.EndTimestamp - df.BeginTimestamp
    df['WaitTime'] = df.BeginTimestamp - df.RequestTimestamp
    df.dropna(subset=['Service'],inplace=True)
    for index, row in df.iterrows():
        if not any(s in row['Service'].lower() for s in SERVICES_LIST):
            df.drop([index],inplace=True)

    df = df[df['Trip or Order Status']=='COMPLETED']
    uber = df.drop(df[df['Service'].str.contains('EAT')].index)
    uber.head(2)
    #lifetime stats
    num_trips = len(uber)
    spend = sum(uber['Cost'])
    nonzero = uber[uber.Cost > 0.0]
    cheapest = nonzero.loc[[nonzero.Cost.idxmin()]]
    expensive = uber.loc[[uber.Cost.idxmax()]]
    closest = uber.loc[[uber.Distance.idxmin()]]
    farthest = uber.loc[[uber.Distance.idxmax()]]
    shortest = uber.loc[[uber.TripTime.idxmin()]]
    longest = uber.loc[[uber.TripTime.idxmax()]]
    avg_wait = uber.WaitTime.mean()

    return {
        'lifetime_trips':num_trips,
        'lifetime_spend':spend,
        'cheapest':cheapest,
        'expensive': expensive,
        'closest': closest,
        'farthest': farthest,
        'shortest': shortest,
        'longest': longest,
        'avg_wait': avg_wait
    }


    # 'piechart': piechart


    #
    # uberx = ((uber.Service.str.findall(r'\b({0})\b'.format('uberx'), flags=re.IGNORECASE)).map(lambda x: len(x)) >  0).sum()
    # uberpool = ((uber.Service.str.findall('pool', flags=re.IGNORECASE)).map(lambda x: len(x)) >  0).sum()
    # uberxl = ((uber.Service.str.findall(r'\b({0})\b'.format('uberxl'), flags=re.IGNORECASE)).map(lambda x: len(x)) >  0).sum()
    # total = len(uber.Service)
    # piechart = plt.pie([uberx, uberpool, uberxl,total-(uberx+uberpool+uberxl)],labels=['UberX','UberPool', 'UberXL', 'Other'])
