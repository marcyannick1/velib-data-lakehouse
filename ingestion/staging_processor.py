import pandas as pd
from datetime import datetime

def process_station_information(snapshot):

    stations = snapshot["data"]["data"]["stations"]

    df = pd.DataFrame(stations)
    df["processed_at"] = datetime.utcnow()

    print(df.columns.tolist())

    return df

def process_station_status(snapshot):

    stations = snapshot["data"]["data"]["stations"]

    df = pd.DataFrame(stations)
    df["processed_at"] = datetime.utcnow()

    print(df.columns.tolist())

    return df