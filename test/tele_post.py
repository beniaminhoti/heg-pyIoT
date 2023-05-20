import requests
from dotenv import load_dotenv
import os


def sendMsg(text, CHAT_ID, BOT_TOKEN):
    url = "https://api.telegram.org/bot{}/sendMessage".format(BOT_TOKEN)

    payload = {
        "text": text,
        "chat_id": CHAT_ID,
    }
    response = requests.post(url, json=payload)
    print(response.text)


def main():
    load_dotenv('.env')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    sendMsg("Coucou", CHAT_ID, BOT_TOKEN)


if __name__ == "__main__":
    main()