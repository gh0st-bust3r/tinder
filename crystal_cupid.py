#!/usr/bin/python

#A little script to make sense of your Tinder data

from datetime import datetime, timedelta
import pandas as pd
import json

#return a list of all days
def init_days(data_days):
    data_days = list(data_days.keys())
    data_days.sort
    strip = '%Y-%m-%d'
    first, last = datetime.strptime(data_days[0], strip), datetime.strptime(data_days[-1], strip)
    all_days = []
    for day in range((last - first).days + 1):
        all_days.append((first + timedelta(days = day)).strftime(strip))
    return all_days

def get_usage(data_file):
    with open(data_file, 'r') as tinder_json:
        data = json.load(tinder_json)
    days = init_days(data['Usage']['app_opens'])
    df = pd.DataFrame(days, columns=['Date'])
    for key in data['Usage'].keys():
        df[key] = df['Date'].map(data['Usage'][key])
    return(df.fillna(0))

def print_weekly(df):
    rows = len(df)
    i = 0
    week = 1
    while(i < rows):
        weekly = df[i:i+7]
        opens = weekly['app_opens'].sum()
        likes = weekly['swipes_likes'].sum()
        passes = weekly['swipes_passes'].sum()
        matches = weekly['matches'].sum()
        messages_in = weekly['messages_received'].sum()
        messages_out = weekly['messages_sent'].sum()
        if(len(weekly) == 7): print('Week %d' % week)
        else: print('Week %d (%d days)' % (week, len(weekly)))
        print('%d likes and %d passes, %.2f%% liked' % (likes, passes, 100 * likes/(passes + likes)))
        print('%d matches, %.2f%% matches per swipe' % (matches, 100 * matches/(passes + likes)))
        print('%d incoming messages, %d outgoing messages' % (messages_in, messages_out))
        print('Opened application %d times\n\n' % opens)
        i += 7
        week += 1

def print_total(df):
    opens = df['app_opens'].sum()
    likes = df['swipes_likes'].sum()
    passes = df['swipes_passes'].sum()
    matches = df['matches'].sum()
    messages_in = df['messages_received'].sum()
    messages_out = df['messages_sent'].sum()
    print('All Time (%d days)' % len(df))
    print('%d likes and %d passes, %.2f%% liked' % (likes, passes, 100 * likes/(passes + likes)))
    print('%d matches, %.2f%% matches per swipe' % (matches, 100 * matches/(passes + likes)))
    print('%d incoming messages, %d outgoing messages' % (messages_in, messages_out))
    print('Opened application %d times\n\n' % opens)

def main():
    df = get_usage('data.json')
    print_weekly(df)
    print_total(df)


main()
