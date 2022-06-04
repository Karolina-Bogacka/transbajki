import os

import requests
import pandas as pd


def get_stations(columns=None):
    if columns is None:
        columns = ['uid', 'lat', 'lng', 'name', 'bike_racks', 'place_type']
    json = requests.get("https://nextbike.net/maps/nextbike-official.json?city=372,210,475").json()
    data = []
    for city in json["countries"][0]['cities']:
        for place in city['places']:
            data.append({col: place[col] for col in columns})
    return pd.DataFrame(data)


def read_bikes(path: str = './data') -> pd.DataFrame:
    bikes = pd.concat([pd.read_csv(os.path.join(path, p)) for p in os.listdir(path)]).reset_index()
    bikes['date'] = pd.to_datetime(bikes['date'])
    bikes['day'] = bikes['date'].dt.floor('d')
    return bikes


def rented_returned_amount(df: pd.DataFrame, stations=get_stations()) -> pd.DataFrame:
    """For each station return number of bikes that were just returned and rented"""
    df_copy= df.copy()
    df_copy['prev_station'] = df_copy \
        .sort_values(by=['date'], kind='stable') \
        .groupby(['bike_number']) \
        .shift(1)['station_id'].astype('Int64')
    df_copy['next_station'] = df_copy \
        .sort_values(by=['date'], kind='stable') \
        .groupby(['bike_number']) \
        .shift(-1)['station_id'].astype('Int64')
    # You can't do next != current because it does not detect loops
    df_copy['just_returned'] = df_copy \
                              .sort_values(by=['date'], kind='stable') \
                              .groupby(['bike_number', 'station_id']) \
                              .shift(1)['date'].isna() | (df_copy['prev_station'] != df_copy['station_id'])
    df_copy['just_rented'] = df_copy \
                            .sort_values(by=['date'], kind='stable') \
                            .groupby(['bike_number', 'station_id']) \
                            .shift(-1)['date'].isna() | (df_copy['next_station'] != df_copy['station_id'])

    grouped = df_copy \
        .groupby(['date', 'station_id']) \
        .aggregate({'bike_number': len, 'just_returned': sum, 'just_rented': sum}) \
        .reset_index() \
        .rename(columns={'bike_number': 'bike_count'}) \
        .merge(stations, left_on='station_id', right_on='uid')
    grouped['just_rented'] = grouped.sort_values(['date']).groupby('station_id').shift(1)['just_rented']
    return grouped.fillna(0)

