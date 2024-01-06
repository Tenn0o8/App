import paho.mqtt.client as paho
from paho import mqtt
import django
import os
import numpy as np


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
django.setup()
print("Setup complete")
from django.conf import settings
from api.models import Device_Info,Device,RSSI_Info
from api.serializers import DeviceInfoSerializer,RSSIInfoSerializer

def get_device(pk):
  return Device.objects.get(pk=pk)

def on_connect(client, userdata, flags, rc, properties=None):
  if rc == 0:
    # client.subscribe("RSSI/#", qos=0)
    client.subscribe("IMU/#", qos=0)
    client.subscribe("CONDITION/#",qos=0)
    client.subscribe("CONDITION_MOD/#",qos=0)
    print("CONNACK received with code %s." % rc)
  else:
    print("Bad connection: ", rc)

def on_subscribe(client,userdata,mid,granted_qos,properties=None):
  print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client,userdata,msg):
  device_topic = msg.topic.rsplit('/')
  if device_topic[0] == 'IMU':
    # khung bản tin gyroR/gyroP/gyroY/accX/accY/accZ/magX/magY/magZ/spinkler
    try:
      content = msg.payload.decode("utf-8")
      content_list = list(map(float,content.split('/')))
      device_id = device_topic[1]

      if len(content_list) == 10:
        payload = {
          'device': device_id,
          'gyroR': content_list[0],
          'gyroP': content_list[1],
          'gyroY': content_list[2],
          'accX': content_list[3],
          'accY': content_list[4],
          'accZ': content_list[5],
          'magX': content_list[6],
          'magY': content_list[7],
          'magZ': content_list[8],
          'spinkler': content_list[9],
        }
        serializer = DeviceInfoSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("Successfully save your data:", content)
      else:
        print("Cannot save your messages, check your data again")

    except:
      print("Cannot save your messages")
  


  if device_topic[0] == 'CONDITION':
    # Khung bản tin: True(False)
    try:
      content = msg.payload.decode("utf-8")
      device_id = device_topic[1]
      current_device = get_device(device_id)
      current_device.condition = eval(content)
      current_device.save()
      return print("Successfuly save your data:",current_device.condition)

    except:
      print("Cannot save your messages")

  if device_topic[0] == 'CONDITION_MOD':
    content = msg.payload.decode("utf-8")
    print("Received message: "+content)

def on_publish(client, userdata, mid, properties=None):
  print("mid: " + str(mid))

    

client = paho.Client(client_id="",userdata=None,protocol=paho.MQTTv5)
client.on_connect = on_connect

client.connect(
  host=settings.MQTT_SERVER,
  port=settings.MQTT_PORT,
  keepalive=settings.MQTT_KEEPALIVE
)

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish 
client.loop_forever()