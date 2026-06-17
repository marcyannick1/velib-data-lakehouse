import json
from datetime import datetime
import tempfile
import pandas as pd
from io import BytesIO

from minio_client import client
from config import BUCKET_NAME

def upload_raw_snapshot(dataset_name, snapshot):

    now = datetime.utcnow()

    object_name = (
        f"raw/"
        f"{dataset_name}/"
        f"{now:%Y}/"
        f"{now:%m}/"
        f"{now:%d}/"
        f"{now:%H%M%S}.json"
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8"
    ) as f:

        json.dump(
            snapshot,
            f,
            ensure_ascii=False,
            indent=2
        )

        temp_path = f.name

    client.fput_object(
        BUCKET_NAME,
        object_name,
        temp_path
    )

    return object_name

def list_objects(prefix):

    return list(
        client.list_objects(
            BUCKET_NAME,
            prefix=prefix,
            recursive=True
        )
    )

def read_json_object(object_name):

    response = client.get_object(
        BUCKET_NAME,
        object_name
    )

    content = response.read()

    return json.loads(content)

def upload_dataframe_csv(dataset_name, dataframe):

    now = datetime.utcnow()

    object_name = (
        f"staging/"
        f"{dataset_name}/"
        f"{now:%Y}/"
        f"{now:%m}/"
        f"{now:%d}/"
        f"{now:%H%M%S}.csv"
    )

    with tempfile.NamedTemporaryFile(
        suffix=".csv",
        delete=False
    ) as f:

        dataframe.to_csv(
            f.name,
            index=False
        )

        client.fput_object(
            BUCKET_NAME,
            object_name,
            f.name
        )

    return object_name

def upload_dataframe_parquet(
    dataset_name,
    dataframe
):

    now = datetime.utcnow()

    object_name = (
        f"curated/"
        f"{dataset_name}/"
        f"{now:%Y}/"
        f"{now:%m}/"
        f"{now:%d}/"
        f"{now:%H%M%S}.parquet"
    )

    with tempfile.NamedTemporaryFile(
        suffix=".parquet",
        delete=False
    ) as f:

        dataframe.to_parquet(
            f.name,
            index=False
        )

        client.fput_object(
            BUCKET_NAME,
            object_name,
            f.name
        )

    return object_name


def read_parquet_object(object_name):

    response = client.get_object(
        BUCKET_NAME,
        object_name
    )

    data = response.read()

    df = pd.read_parquet(
        BytesIO(data)
    )

    return df