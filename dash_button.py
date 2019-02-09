#!/usr/bin/env python3
# coding:utf-8
import smbus
import time
from gpiozero import Button
import requests
import json
import sys
import datetime


lcd_clear = 0x01
lcd_home = 0x02
lcd_newline = 0xc0

i2c = smbus.SMBus(1)

def lcd_command(code):
    i2c.write_byte_data(0x3e,0,code)
    time.sleep(0.1)

def lcd_init ():
    
    sys.stderr.write("Starting Dash Button...\n")
    lcd_command(0x38)
    lcd_command(0x39)
    lcd_command(0x14)
    lcd_command(0x73)
    lcd_command(0x56)
    lcd_command(0x6c)
    lcd_command(0x38)
    lcd_command(lcd_clear)
    lcd_command(lcd_home)
    sys.stderr.write("Started Dash Button...\n")

def lcd_print (line1,line2):
    lcd_command(lcd_clear)
    lcd_command(lcd_home)
    
    message=[line1,line2]

    for line in message:
        
        linelist=[]
        
        for c in line:
            linelist.append(ord(c))
        
        i2c.write_i2c_block_data(0x3e,0x40,linelist)
        time.sleep(0.1)
        lcd_command(lcd_newline)
        time.sleep(0.1)

def write_log(text):
    utctime = datetime.datetime.now(datetime.timezone.utc)
    timestamp=utctime.replace(microsecond=0).astimezone().isoformat()
    
    f=open('/home/pi/dash_button_log.csv','a')
    f.write(timestamp+","+text+'\n')
    f.close()
    
#main
lcd_init()
write_log("started")
lcd_print("Dash","Button")

button = Button(26)
quit_key=Button(19)

while True:
    if button.is_pressed:
        
        lcd_print("Message","sent!")
        
        # rewrite API key
        requests.post('https://hooks.slack.com/services/custom-integration-key', data = json.dumps({
            'text': u'差し入れください',
            'username': u'差し入れDash Button',
            'icon_emoji': u':candy:',
            'link_names': 1,
        }))
        write_log("Button pushed")
        time.sleep(10)
        
        lcd_print("Dash","Button")
    if quit_key.is_pressed:
        lcd_print("Quit","Button")
        lcd_command(lcd_clear)
        write_log("exited")
        exit()


