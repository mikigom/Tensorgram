import json
import requests
import time
import urllib
import telegram
import os
from urllib import quote
import requests.packages.urllib3
import tensorboard_listen

requests.packages.urllib3.disable_warnings()

TOKEN = "373979783:AAFgtFdIGsF6p-ZNL3fC2siUjKiSXXqmIpU"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot = telegram.Bot(token=TOKEN)
#global last_update_id = None

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
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_return(file_name, updates, caption):
    for update in updates["result"]:
        chat = update["message"]["chat"]["id"]
        sendImage(file_name, chat, caption)

def sendImage(loss_name, chat_id, caption):
    print(bot.sendPhoto(chat_id=chat_id, photo=open("./tmp/" + str(loss_name) + ".png", "rb"), caption = caption))

def listen_and_response():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            tensorboard_listen.open_and_init_driver()
            tensorboard_listen.save_screenshot()
            try:
                if updates["result"][0]["message"]["text"] == "all":
                    for file in os.listdir(os.getcwd() + "/tmp"):
                        file_ = file.rsplit('.', 1)[0]
                        send_return(file_, updates, file_)
                else:
                    last_update_id = get_last_update_id(updates) + 1
                    send_return(updates["result"][0]["message"]["text"], updates, updates["result"][0]["message"]["text"])
            except:
                send_message("Cannot find any matched summary name.", updates["result"][0]["message"]["chat"]["id"])
            tensorboard_listen.close_driver()
        time.sleep(1)

if __name__ == '__main__':
    print("Listen...")
    listen_and_response()
