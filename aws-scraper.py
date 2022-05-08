import requests
import datetime
import pandas as pd
import boto3

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('rowerki')
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    json = requests.get("https://nextbike.net/maps/nextbike-official.json?city=372,210,475").json()
    data = []
    for city in json["countries"][0]['cities']:
        for place in city['places']:
            for bike in place['bike_list']:
                data.append((date, place['uid'], bike["number"], bike["bike_type"], bike["state"]))
    csv = pd.DataFrame(data, columns=['date', 'station_id', "bike_number", "bike_type", "state"]).to_csv(index=False)
    s3_obj = s3.Object("rowerki", str(int(datetime.datetime.now().timestamp())) + '.csv')
    s3_obj.put(Body=csv)
