from pymongo import MongoClient
from pandas import DataFrame
import pandas as pd
import datetime
import time
import urllib
import config
def getdatamongo(date_from,date_to, relevant ):
    timestamp_from = date_from.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
    timestamp_to = date_to.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
    connection_string = '' # DATABASE CREDENTIALS
    client = MongoClient(connection_string)
    database=client[''] # DATABASE NAME
    tweets = database.get_collection(config.COLLECTION)
    a = tweets.find({"timestamp_ms_long": {"$gte": timestamp_from, "$lte": timestamp_to}, "lang": 'es', "location": {"$exists": True}},{'user': 1, 'entities': 1,  "_id": 0})
    pairs = []
    for tweet in a:
        user = tweet['user']
        entities = tweet['entities']
        if 'user_mentions' in entities:
            user_mentions = entities['user_mentions']
            for i in range(len(user_mentions)):
                user_mention = user_mentions[i]
                pairs.append([str(user['id_str']), str(user_mention['id_str'])])
    return pairs
