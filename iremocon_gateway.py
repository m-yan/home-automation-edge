#-*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import socket
import config

broker_ip = config.get("mqtt_broker", "ip")
broker_port = config.getint("mqtt_broker", "port")
sub_topic = config.get("mqtt_client", "sub_topic")

iremocon_ip = config.get("iremocon", "ip")
iremocon_port = config.getint("iremocon", "port")


def on_connect(client, userdata, flags, respons_code):
    client.subscribe(sub_topic)

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
    try:
        userdata.send(msg.payload + b'\r\n')
        print(userdata.recv(4096))
    except socket.error:
        userdata.close()
        sock = get_iremocon_connection()
        self.user_data_set(sock)

def get_iremocon_connection():
    sock = socket.create_connection((iremocon_ip, iremocon_port), timeout=5)
    sock.settimeout(None)
    return sock

try:
    sock = get_iremocon_connection()
    client = mqtt.Client(protocol=mqtt.MQTTv311, userdata=sock)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_ip, port=broker_port, keepalive=60)
    client.loop_forever()

except KeyboardInterrupt:
    sock.close()
    client.disconnect()
