#-*- coding: utf-8 -*-
import motion_sensor
import paho.mqtt.client as mqtt
import socket

MQTT_BROKER = '13.78.50.153'
MQTT_BROKER_PORT = 1883
MQTT_CLIENT_ID = 'AE:ASN-AE'
PUB_TOPIC = 'oneM2M/req/ASN-AE/IN-CSE/json'
SUB_TOPIC = 'oneM2M/req/IN-CSE/ASN-AE/json'

IREMOCON = '192.168.11.7'
IREMOCON_PORT = 51013

def on_connect(client, userdata, flags, respons_code):
  client.subscribe(SUB_TOPIC)

def on_message(client, userdata, msg):
  print(msg.topic + ' ' + str(msg.payload))
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((IREMOCON, IREMOCON_PORT))
  sock.send(msg.payload + b'\r\n')
  print(sock.recv(4096))
  sock.close()

def on_detected():
  print("人を感知しました")
  client.publish(PUB_TOPIC, '1')

def on_undetected():
  print("人がいなくなりました")
  client.publish(PUB_TOPIC, '0')


client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=False, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, port=MQTT_BROKER_PORT, keepalive=60)
client.loop_start()


h_sensor = motion_sensor.HumanDetector();
h_sensor.monitor(on_detected, on_undetected)
