import pandas as pd


def build_station_dimension(df):

    df = df.rename(
        columns={
            "stationCode": "station_code",
            "lat": "latitude",
            "lon": "longitude"
        }
    )

    columns = [
        "station_id",
        "station_code",
        "name",
        "latitude",
        "longitude",
        "capacity"
    ]

    return df[columns]



def build_station_status_fact(df):

    # extraction du nombre de vélos électriques
    # depuis le JSON Vélib

    df["num_ebikes_available"] = (
        df["num_bikes_available_types"]
        .apply(
            lambda x: x.get("ebike", 0)
            if isinstance(x, dict)
            else 0
        )
    )

    columns = [
        "station_id",
        "num_bikes_available",
        "num_ebikes_available",
        "num_docks_available",
        "last_reported"
    ]

    return df[columns]