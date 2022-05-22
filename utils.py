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
