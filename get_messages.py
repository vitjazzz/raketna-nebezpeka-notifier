from telethon import TelegramClient, events
from playsound import playsound
import requests
import time

API_ID = 666
API_HASH = ""
PHONE_NUMBER = ""
CHANNEL = ""

PUSHCUT_API_KEY = ""
NOTIFICATION_NAME = "My%20First%20Notification"
headers = {
    "Content-Type": "application/json"
}

url = f"https://api.pushcut.io/{PUSHCUT_API_KEY}/notifications/{NOTIFICATION_NAME}"

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
            requests.post(url, headers=headers)
            playsound('alarm.wav')
            playsound('alarm.mp3')
            time.sleep(5)
            requests.post(url, headers=headers)
        else:
            print("No matching keywords in the message.")
    else:
        print("Received a message with no text.")
    

print("Listening for new messages...")
client.run_until_disconnected()