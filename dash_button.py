#!/usr/bin/env python3
import datetime
import json
import os
import sys
import time
import datetime

import requests
from gpiozero import Button

install_dir = '/home/pi/present-dash-button/'


def write_log(text):
    print(text)

    utctime = datetime.datetime.now(datetime.timezone.utc)
    timestamp = utctime.replace(microsecond=0).astimezone().isoformat()
    f = open(install_dir+'log.csv', 'a')
    f.write(timestamp+","+text+'\n')
    f.close()


# main
if __name__ == "__main__":

    print("starting present-dash-button.")

    token = ""
    downtime = 600

    pre_time = datetime.datetime(2018, 1, 1)
    now_time = datetime.datetime.now()

    try:
        with open(str(install_dir+"settings.json")) as f:
            json_data = json.load(f)
            token = json_data["SLACK_TOKEN"]
    except FileNotFoundError:
        sys.stderr.write('Settings.json not found!\n')
        sys.exit(1)

    button = Button(2)

    write_log("started")

    while True:
        if button.is_pressed:
            now_time = datetime.datetime.now()
            if now_time - pre_time >= datetime.timedelta(seconds=downtime):
                pre_time=now_time
                requests.post(token, data=json.dumps({'text': u'只今調整中'}))
                write_log("Button pushed")
