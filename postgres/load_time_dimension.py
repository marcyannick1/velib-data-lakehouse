from datetime import datetime, timedelta

from sqlalchemy import text

from connection import engine



def load_time_dimension():

    start = datetime(2026,1,1)
    end = datetime(2027,1,1)


    rows = []

    current = start

    while current < end:

        rows.append({
            "date_time": current,
            "date": current.date(),
            "hour": current.hour,
            "day": current.day,
            "month": current.month,
            "year": current.year,
            "day_of_week": current.weekday()
        })

        current += timedelta(hours=1)


    query = text(
        """
        INSERT INTO dim_time
        (
            date_time,
            date,
            hour,
            day,
            month,
            year,
            day_of_week
        )

        VALUES
        (
            :date_time,
            :date,
            :hour,
            :day,
            :month,
            :year,
            :day_of_week
        )

        ON CONFLICT DO NOTHING
        """
    )


    with engine.begin() as conn:

        conn.execute(
            query,
            rows
        )


if __name__ == "__main__":

    load_time_dimension()

    print("dim_time remplie")