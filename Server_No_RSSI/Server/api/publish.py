import paho.mqtt.client as mqtt

broker_address = "192.168.1.103"
broker_port = 1883
condition_topic = "CONDITION/#"  

def publish(message,topic,broker_address=broker_address,broker_port = broker_port):
  client = mqtt.Client()
  client.connect(broker_address, broker_port, 60)
  client.publish(topic, message)
  client.disconnect()

def Condition_publish(condition,id):
  topic = "CONDITION_MOD/" + str(id) 
  print(condition)
  publish(condition,topic)

