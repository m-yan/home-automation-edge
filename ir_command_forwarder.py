#-*- coding: utf-8 -*-

import iremocon_util
import paho.mqtt.client as mqtt
import config
from onem2m_util import extract_notify_cin_con


def __on_connect(client, irgw, flags, rc):
    client.subscribe(sub_topic)


def __on_message(client, irgw, message):
    str_payload = message.payload.decode('utf-8')
    print(message.topic + ' ' + str_payload)

    iremocon_command = extract_notify_cin_con(str_payload)
    print(iremocon_command)
    if iremocon_command is None:
        return

    irgw.send_command(iremocon_command)


def __on_disconnect(client, irgw, rc):
    irgw.close()


if __name__ == '__main__':
    broker_ip = config.get('mqtt_broker', 'ip')
    broker_port = config.getint('mqtt_broker', 'port')
    sub_topic = config.get('mqtt_client', 'sub_topic')

    irgw = iremocon_util.IRemoconGW()

    try:
        client = mqtt.Client(protocol=mqtt.MQTTv311, userdata=irgw)
        client.on_connect = __on_connect
        client.on_message = __on_message
        client.on_disconnect = __on_disconnect

        client.connect(broker_ip, port=broker_port, keepalive=60)
        print('Connected sucessfully to MQTT Broker.')

        client.loop_forever()

    finally:
        client.disconnect()
        print('Connection to MQTT Broker closed.')
