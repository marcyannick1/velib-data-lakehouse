import sys
import os

sys.path.append(
    "/opt/project"
)

from sqlalchemy import text

from postgres.connection import engine


def get_station_alerts():

    query = text(
        """
        SELECT
            station_id,
            station_code,
            name,
            bikes_available,
            docks_available,
            alert_status,
            event_time

        FROM vw_station_alert
        """
    )


    with engine.connect() as conn:

        result = conn.execute(query)

        return result.fetchall()



def generate_message(alerts):

    if not alerts:

        return "✅ Toutes les stations sont normales"


    message = (
        f"🚨 {len(alerts)} station(s) critique(s)\n\n"
    )


    for alert in alerts:

        message += (
            f"📍 {alert.name}\n"
            f"🚲 vélos : {alert.bikes_available}\n"
            f"🅿️ places : {alert.docks_available}\n"
            f"⚠️ {alert.alert_status}\n\n"
        )


    return message



if __name__ == "__main__":

    alerts = get_station_alerts()

    message = generate_message(alerts)

    print(message)