import requests, json, time,random

url = 'http://thingworx-eng.tp.edu.sg/Thingworx/Things/PE05_3_PiThing/Properties/Temperature'

#The appKey has been edited

headers = {'content-type': 'application/json',
           'appKey': '360a9e5c-8eb8-4cec-a6e3-b87a2ac8aa7d'}
           
def ThingWorx():
    payload = {'Temperature': getSensorData()}
    print("ttt")
    r = requests.put(url, data=json.dumps(payload),headers=headers)
