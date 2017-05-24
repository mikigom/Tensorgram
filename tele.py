import json
import requests
import time
import urllib
import telegram
from urllib import quote

TOKEN = "373979783:AAFgtFdIGsF6p-ZNL3fC2siUjKiSXXqmIpU"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = telegram.Bot(token=TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    print(content)
    return content

def post_url(url):
    response = requests.post(url)
    content = response.content.decode("utf8")
    print(content)
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    print(chat_id)
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_return(file_name, updates):
    for update in updates["result"]:
        print("hit!")
        chat = update["message"]["chat"]["id"]
        sendImage(file_name, chat)

def sendImage(file_name, chat_id, caption):
    print(bot.sendPhoto(chat_id=chat_id, photo=open("./test.png", "rb"), caption = caption))

def listen_and_response():
    while True:
        try:
            updates = get_updates(last_update_id)
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                send_return('./test.png', updates, caption)
            time.sleep(0.5)
        except:
            pass
