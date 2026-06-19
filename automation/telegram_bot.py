import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from sqlalchemy import text

from postgres.connection import engine


TOKEN = os.getenv("TELEGRAM_TOKEN")


# ==========================
# KPI GLOBAL
# ==========================

async def kpi(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = text(
        """
        SELECT *
        FROM vw_global_kpi
        """
    )

    with engine.connect() as conn:

        result = conn.execute(query).fetchone()

    message = (
        f"📊 KPI Vélib\n\n"
        f"🚉 Stations : {result.total_stations}\n"
        f"🚲 Vélos : {result.total_bikes}\n"
        f"⚡ E-bikes : {result.total_ebikes}\n"
        f"🅿️ Places libres : {result.total_free_docks}\n"
        f"📈 Moyenne vélos/station : {result.avg_bikes_per_station}\n"
        f"🕒 Dernière mise à jour : {result.last_update}"
    )

    await update.message.reply_text(message)


# ==========================
# ALERTES
# ==========================

async def alertes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = text(
        """
        SELECT *
        FROM vw_station_alert
        LIMIT 20
        """
    )

    with engine.connect() as conn:

        alerts = conn.execute(query).fetchall()

    if not alerts:

        await update.message.reply_text(
            "✅ Aucune alerte"
        )
        return

    message = "🚨 Alertes Vélib\n\n"

    for alert in alerts:

        message += (
            f"📍 {alert.name}\n"
            f"🚲 {alert.bikes_available}\n"
            f"🅿️ {alert.docks_available}\n"
            f"⚠️ {alert.alert_status}\n\n"
        )

    await update.message.reply_text(message[:4000])


# ==========================
# TOP STATIONS
# ==========================

async def stations(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = text(
        """
        SELECT
            name,
            bikes_available
        FROM vw_station_availability
        ORDER BY bikes_available DESC
        LIMIT 10
        """
    )

    with engine.connect() as conn:

        rows = conn.execute(query).fetchall()

    message = "🏆 Top 10 stations\n\n"

    for row in rows:

        message += (
            f"📍 {row.name}\n"
            f"🚲 {row.bikes_available}\n\n"
        )

    await update.message.reply_text(message)


# ==========================
# START
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
🚲 Bot Vélib

Commandes disponibles :

/kpi
/stations
/alertes
        """
    )


# ==========================
# MAIN
# ==========================

def main():

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("kpi", kpi)
    )

    app.add_handler(
        CommandHandler("stations", stations)
    )

    app.add_handler(
        CommandHandler("alertes", alertes)
    )

    print("Bot démarré")

    app.run_polling()


if __name__ == "__main__":
    main()