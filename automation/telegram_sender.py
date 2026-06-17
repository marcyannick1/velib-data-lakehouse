import requests
import os


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_message(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{TOKEN}/sendMessage"
    )


    # découpe Telegram max ~4000 caractères
    chunks = [
        message[i:i+4000]
        for i in range(0, len(message), 4000)
    ]


    for chunk in chunks:

        payload = {
            "chat_id": CHAT_ID,
            "text": chunk
        }


        response = requests.post(
            url,
            json=payload
        )

        response.raise_for_status()


    print("Message Telegram envoyé")