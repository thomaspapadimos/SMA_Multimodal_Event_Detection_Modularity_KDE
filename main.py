import pandas as pd
from GettingDataFromMongo import  getdatamongo
from sklearn.neighbors import KernelDensity
import subprocess
import numpy as np
from statistics import mean
import urllib
import matplotlib.pyplot as plt
import statistics
import datetime
import time
from pymongo import MongoClient
import matplotlib as mpl
from scipy.signal import find_peaks
import config
import time

def temp_feature(df):
    import statistics
    time_sub = [(datetime.datetime.fromtimestamp(int(df.timestamp_ms_long[len(df)-1])/1000) - datetime.datetime.fromtimestamp(int(df.timestamp_ms_long[i])/1000)) for i in range(len(df))]
    hour = list(map((lambda  x : x.total_seconds()/ 3600), time_sub))
    v = []
    for x in hour:
        v.append(x)
    h = (4 * (statistics.stdev(v) ** 5) / 3 * len(hour)) ** (-1 / 5)
    kde = KernelDensity(kernel='gaussian', bandwidth=h)
    #kde = KernelDensity(kernel='gaussian')
    hour = (np.array(hour))[:, np.newaxis]
    kde.fit(hour, y=None)
    log_dens = kde.score_samples(hour)
    kde_eval = np.exp(log_dens)
    return max(kde_eval)

def days_to_tmstmp(date_from,date_to):

    d_from = datetime.datetime(date_from[0], date_from[1], date_from[2])
    d_to = datetime.datetime(date_to[0], date_to[1], date_to[2])
    #days.append(d_to.strftime('%m-%d'))
    # print("Unix_Time_stamp: ", (time.mktime(date.timetuple())))
    timestamp_from = time.mktime(d_from.timetuple())
    timestamp_from = int(timestamp_from)

    timestamp_to = time.mktime(d_to.timetuple())
    timestamp_to = int(timestamp_to)

    return timestamp_from,timestamp_to

def event_detection(date,r,R_kde,days):
   for date in dates:
        date += datetime.timedelta(days=1)
        date_target = date - datetime.timedelta(days=1)
        print(date)
        relevant = False
        modularity = []
        kde = []
        days = []
        for d in range(r):
            date_from = date - datetime.timedelta(days=r-d)
            date_to = date - datetime.timedelta(days=r-d-1)
            #-------CREATE user_pairs FILE-------
            start_time = time.time()
            user_pairs = getdatamongo(date_from,date_to,relevant)
            print("---USER_PAIRS Created in %s seconds ---" % (time.time() - start_time))
            del start_time
            df = pd.DataFrame(user_pairs)
            df.to_csv('user_pairs.csv', sep=';', header=None, index=False)
            del df, user_pairs
            #------MODULARITY SCORE CALCULATION--------
            try:
                mod_score = float(subprocess.check_output(['Rscript' , 'community_detection_expiriments.R']))
                modularity.append(mod_score)

            except:
                modularity.append(0)
            days.append(date_from.strftime('%m-%d'))
            connection_string = '' #DATABASE CREDENTIALS ---------!!!!!!!!!!!!!!
            client = MongoClient(connection_string)
            database=client[''] #DATABASE NAME --------------!!!!!!!!!
            tweets = database.get_collection(config.COLLECTION)
        #--------KDE CALCULATION----------
            date_from = date - datetime.timedelta(days=r-d+R_kde)
            date_to = date - datetime.timedelta(days=r-d-1)
            timestamp_from = date_from.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
            timestamp_to = date_to.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
            a = tweets.find({"timestamp_ms_long": {"$gte": timestamp_from, "$lte": timestamp_to}, "lang": 'es', "location": {"$exists": True}},
                               {'full_text': 1, 'timestamp_ms_long': 1, "_id": 0})
            df = pd.DataFrame(a)
            try:
                kde.append(temp_feature(df))
            except:
                kde.append(0)
        modularity_array = np.array(modularity)
        m_peaks, _ = find_peaks(modularity_array, height=0)
        m_peaks2, _ = find_peaks(-modularity_array)
        kde_array = np.array(kde)
        peaks, _ = find_peaks(kde_array, height=0)
        peaks2, _ = find_peaks(-kde_array)
        flag=True
        if kde[1]>kde[0]:
            if modularity[1]<modularity[0]:
                flag=True
        if flag:
            print('EVENT FOUND!!')
            color = ['#00429d', '#2754a6', '#3a67ae', '#487bb7', '#548fc0',
                     '#5ea3c9', '#66b8d3', '#6acedd', '#68e5e9', '#ffe2ca',
                     '#ffc4b4', '#ffa59e', '#f98689', '#ed6976', '#dd4c65',
                     '#ca2f55', '#b11346', '#93003a']
            mpl.style.use('seaborn')
            fig, axs = plt.subplots(2)
            fig.set_size_inches(15, 8)
            fig.suptitle('Vertically stacked subplots')
            axs[0].plot(days, modularity, label='modularity score', color=color[10])
            axs[0].plot(m_peaks, modularity_array[m_peaks], 'o')
            axs[0].plot(m_peaks2, modularity_array[m_peaks2], 'o')
            axs[0].legend()
            axs[1].plot(days, kde, label='kde score', color=color[1])
            axs[1].plot(peaks, kde_array[peaks], 'o')
            axs[1].plot(peaks2, kde_array[peaks2], 'o')
            axs[1].legend()
            fig.savefig('images/{} modularity_kde.png'.format(date_target.strftime('%m-%d')),
                        bbox_inches='tight', dpi=100)
            del fig, axs
            timestamp = date_target.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
            date_target2 = date - datetime.timedelta(days=1)
            timestamp2 = date_target2.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
            df_tweets_target = df.loc[df['timestamp_ms_long'] > timestamp]
            df_tweets_target = df.loc[df['timestamp_ms_long'] < timestamp2]
            texts = df_tweets_target['full_text'].values
            target_dict = {"date": date_target, "ms_score": modularity[1], 'kde_score': kde[1], 'texts': texts.tolist()}
            #---STORE  TO DATABASE---
            mycol = database['SpanishFires_Events_MS_KDE_RKDE1']
            x = mycol.insert_one(target_dict)
        del df

dates = [datetime.datetime(2019, 5, 16),datetime.datetime(2019, 6, 2),datetime.datetime(2019, 6, 27),
         datetime.datetime(2019, 6, 29),datetime.datetime(2019, 7, 14),datetime.datetime(2019, 7, 24),datetime.datetime(2019, 8, 5),datetime.datetime(2019, 8, 11),datetime.datetime(2019, 8, 13)]

date = datetime.datetime(2018, 1, 1)
r = 5  # DONT CHANGE:  range before the date for the whole visualization IF CHANGE, GO CHANGE THE RULE
R_kde = 1  # range before the date for the kde
days = 10 #days to run from date
event_detection(dates,r,R_kde,days)