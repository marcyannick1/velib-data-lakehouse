import sys
import os
import pandas as pd

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import MetaData, Table


sys.path.append(
    os.path.abspath("../ingestion/src")
)


from storage import read_parquet_object

from minio_client import client

BUCKET_NAME = "velib-lake"

from connection import engine



def load_station_dimension(parquet_path):

    df = read_parquet_object(
        parquet_path
    )


    df = df.rename(
        columns={
            "stationCode": "station_code",
            "lat": "latitude",
            "lon": "longitude"
        }
    )


    records = df.to_dict(
        orient="records"
    )


    metadata = MetaData()


    table = Table(
        "dim_station",
        metadata,
        autoload_with=engine
    )


    with engine.begin() as conn:

        for record in records:

            stmt = insert(table).values(
                **record
            )


            stmt = stmt.on_conflict_do_update(
                index_elements=[
                    "station_id"
                ],

                set_={
                    "station_code":
                        stmt.excluded.station_code,

                    "name":
                        stmt.excluded.name,

                    "latitude":
                        stmt.excluded.latitude,

                    "longitude":
                        stmt.excluded.longitude,

                    "capacity":
                        stmt.excluded.capacity
                }
            )


            conn.execute(stmt)



def load_station_status(parquet_path):

    df = read_parquet_object(
        parquet_path
    )


    df = df.rename(
        columns={
            "num_bikes_available":
                "bikes_available",

            "num_ebikes_available":
                "ebikes_available",

            "num_docks_available":
                "docks_available"
        }
    )


    df["event_time"] = pd.Timestamp.now()


    columns = [
        "station_id",
        "bikes_available",
        "ebikes_available",
        "docks_available",
        "last_reported",
        "event_time"
    ]


    df = df[columns]


    df.to_sql(
        "fact_station_status",
        engine,
        if_exists="append",
        index=False
    )



def get_latest_parquet(prefix):

    objects = client.list_objects(
        BUCKET_NAME,
        prefix=prefix,
        recursive=True
    )


    files = [
        obj.object_name
        for obj in objects
        if obj.object_name.endswith(".parquet")
    ]


    if not files:
        raise Exception(
            f"No parquet found in {prefix}"
        )


    return sorted(files)[-1]



if __name__ == "__main__":


    station_information_file = get_latest_parquet(
        "curated/station_information/"
    )


    station_status_file = get_latest_parquet(
        "curated/station_status/"
    )


    print(
        "Loading:",
        station_information_file
    )


    print(
        "Loading:",
        station_status_file
    )


    load_station_dimension(
        station_information_file
    )


    load_station_status(
        station_status_file
    )


    print(
        "Postgres loading completed"
    )