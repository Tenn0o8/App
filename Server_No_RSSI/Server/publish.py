import paho.mqtt.client as mqtt
# from datasets.data_retrieaver import train_data,valid_data,test_data


# Define MQTT broker settings
# broker_address = "127.0.0.1"
broker_address = "192.168.1.103"
broker_port = 1883
rssi_topic = "RSSI/#"
imu_topic = "IMU/#"  
condition_topic = "CONDITION/#"  
ap_number = 5

def publish(message,topic,broker_address=broker_address,broker_port = broker_port):
  client = mqtt.Client()
  client.connect(broker_address, broker_port, 60)
  client.publish(topic, message)
  client.disconnect()
  print("Published:",message)

# 7: 40_4v1
# 8: 34_4v2
# 9: 34_5v3


rssi_topic = 'RSSI/9'
rssimessage = '-35/-50/-52/-54/-48'
# khung bản tin RSSI1/RSSI2/RSSI3/RSSI4/RSSI5/...

IMU_topic = 'IMU/9'
imumessage = '7/7/7/7/7/7/7/7/7'
# khung bản tin gyroR/gyroP/gyroY/accX/accY/accZ/magX/magY/magZ

CONDITION_topic = 'CONDITION/9'
conditionmessage = 'True'
# Khung bản tin: True(False)

# [[-43. -54. -53. -54. -43.]
#  [-43. -53. -52. -56. -41.]
#  [-39. -54. -51. -54. -51.]
#  [-38. -55. -44. -55. -49.]
#  [-38. -51. -54. -55. -50.]
#  [-35. -50. -52. -54. -48.]
#  [-36. -54. -52. -59. -45.]
#  [-35. -52. -46. -55. -50.]
#  [-45. -74. -55. -57. -41.]
#  [-39. -52. -54. -56. -50.]]



# print(train_data[100:110,:ap_number])
# print(train_data[100:110,ap_number])

publish(rssimessage,rssi_topic)
publish(imumessage,IMU_topic)
publish(conditionmessage,CONDITION_topic)
