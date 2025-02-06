from telethon import TelegramClient, events
from playsound import playsound
import requests
import time
import asyncio

from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
CHANNEL = os.getenv("CHANNEL")
CONTROL_CHANNEL = os.getenv("CONTROL_CHANNEL")

PUSHCUT_API_KEY = os.getenv("PUSHCUT_API_KEY")
NOTIFICATION_NAME = "My%20First%20Notification"
headers = {
    "Content-Type": "application/json"
}

base_url_format = "https://api.pushcut.io/{key}/notifications/{notification_name}"
pushcut_keys = [key.strip() for key in PUSHCUT_API_KEY.split("|")]
urls = [base_url_format.format(key=key, notification_name=NOTIFICATION_NAME) for key in pushcut_keys]

keywords = ['ракет', 'зліт', 'балістик', 'центр', 'берестей', 'лук\'янівка', 'поділ', 'липки']


# Create the Telethon client
client = TelegramClient("session_name", API_ID, API_HASH)

client.start(PHONE_NUMBER)

@client.on(events.NewMessage(chats=CHANNEL))
async def new_message_handler(event):
    text = event.raw_text
    if text:
        lower_text = text.lower()
        if any(keyword in lower_text for keyword in keywords):
            print("Keyword detected! Playing sound.")
            for url in urls:
                requests.post(url, headers=headers)
            playsound('alarm.mp3')
            time.sleep(5)
            for url in urls:
                requests.post(url, headers=headers)
        else:
            print("No matching keywords in the message.")


message_text = f"Аналізую канал '{CHANNEL}', підписників - {len(urls)}."

async def send_message_periodically():
    while True:
        try:
            await client.send_message(CONTROL_CHANNEL, message_text)
        except Exception as e:
            print("Error sending message:", e)
        await asyncio.sleep(2 * 3600)


with client:
    client.loop.run_until_complete(send_message_periodically())

print("Listening for new messages...")
client.run_until_disconnected()