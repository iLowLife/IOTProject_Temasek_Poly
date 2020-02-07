import datetime
import paho.mqtt.client as mqtt
import os
import telepot   # Importing the telepot library
from telepot.loop import MessageLoop    # Library function to communicate with telegram bot
from time import sleep
from datetime import datetime

import RPi.GPIO as GPIO
import smbus2
import bme280
from mqtt_sub import *
from ThingWorx import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

bot = telepot.Bot('1070851315:AAEpZlSQNsGtJ7efwcNM1Yu6gGfsBo6mS2U')
print (bot.getMe())

port = 1
address = 0x76
bus = smbus2.SMBus(port)

mqtt_broker = "mqtt.eclipse.org"
topic = "ilowlife/1"

def main():
    StartMQTT()
    while True:
        
        MessageLoop(bot, handle).run_as_thread()
        #ThingWorx()
        GPIO.output(4,GPIO.HIGH)
        calibration_params = bme280.load_calibration_params(bus, address)

        data = bme280.sample(bus, address, calibration_params)
    
        temp1 = data.temperature
        pay_load = "Temp =" + str(temp1)    
    
        my_mqtt = mqtt.Client()
    
        my_mqtt.connect(mqtt_broker,port=1883)
        print("--connected to broker")        
        
        try:
            my_mqtt.publish(topic, pay_load)
            print("--Temp = %.1f" % temp1)
        except:
            print("--error")
        else:
            print("--disconnected")
        time.sleep(2)

def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print ('Received:')
    print(command)
    
    global FanCount
    
    now = datetime.now()
    # Comparing the incoming message to send a reply according to it
    if command == '/Hi':
        bot.sendMessage (chat_id, str("Hi! Low"))
    elif command == '/Time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/Date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    # For the Project from Light and Fan
    elif command == '/Light_1':
        bot.sendMessage(chat_id, str("LIGHT is ON"))
        GPIO.output(17,GPIO.HIGH)
    
    elif command == '/Light_0':
        bot.sendMessage(chat_id, str("LIGHT is OFF"))
        GPIO.output(17,GPIO.LOW)
    elif command == '/Fan':
        FanCount = FanCount + 1
        GPIO.output(4,GPIO.LOW)
        bot.sendMessage(chat_id, str(FanCount))
        if (FanCount % 2) == 1:
            bot.sendMessage(chat_id, str("FAN is ON"))
            print("Fan On")
            #os.system('mpg123 /home/pi/Desktop/Project/FanOn.mp3 &')
    
        elif (FanCount % 2) == 0:
            bot.sendMessage(chat_id, str("FAN is OFF"))
            print("Fan Off")
            #os.system('mpg123 /home/pi/Desktop/Project/FanOff.mp3 &')
        
if __name__ == "__main__":
    main()
