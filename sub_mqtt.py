import time
import paho.mqtt.client as mqtt
import psutil
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

mqtt_broker = "mqtt.eclipse.org"
topic2 ="ilowlife/2"

FanCount = 0
LightCount = 0
my_mqtt2 = None

def onMessage(client,userdata,message):
    global FanCount
    global LightCount
    print("%s %s" % (message.topic, message.payload))
    if message.payload:
        variable = message.payload.decode("utf-8")
        threshhold = int(variable)
        print(threshhold)
        if(threshhold == 1):
            FanCount = FanCount + 1
            print(FanCount)
            GPIO.output(4,GPIO.LOW)
            if((FanCount % 2) == 1):
                print("Fan On")
                #os.system('mpg123 /home/pi/Project/FanOn.mp3 &')
            elif((FanCount % 2) == 0):
                print("Fan Off")
                #os.system('mpg123 /home/pi/Project/FanOff.mp3 &')
        elif(threshhold == 2):
            LightCount = LightCount +1
            print(LightCount)
            if((LightCount % 2) == 1):
                print("Light On")
                GPIO.output(17,GPIO.HIGH)
                os.system('mpg123 /home/pi/Project/LightOn.mp3 &')
            elif((LightCount % 2) == 0):
                print("Light Off")
                os.system('mpg123 /home/pi/Project/LightOff.mp3 &')
                GPIO.output(17,GPIO.LOW)
                
def StartMQTT():
    my_mqtt2 = mqtt.Client()
    my_mqtt2.on_message = onMessage
    
    my_mqtt2.connect(mqtt_broker,port=1883)
    my_mqtt2.subscribe(topic2,qos=1)
    my_mqtt2.loop_start()
    print("Sub to topic")
