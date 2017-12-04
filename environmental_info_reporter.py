#-*- coding: utf-8 -*-

import iremocon_util
import config
import paho.mqtt.client as mqtt
from onem2m_util import create_upload_request
from time import sleep


broker_ip = config.get('mqtt_broker', 'ip')
broker_port = config.getint('mqtt_broker', 'port')

pub_topic = config.get('mqtt_client', 'pub_topic')

to = config.get('container_uri', 'environmental_data')

measure_interval_sec = config.getint('environmental_sensor', 'measure_interval_sec')

client = mqtt.Client(protocol=mqtt.MQTTv311)

irgw = iremocon_util.IRemoconGW()

try:
    while True:
        temperature = irgw.get_temperature()
        humidity = irgw.get_humidity()
        illuminance = irgw.get_illuminance()

        contents = u'{{\\"temperature\\": {}, \\"humidity\\": {}, \\"illuminance\\": {}}}'.format(temperature,humidity,illuminance)

        try:
            client.connect(broker_ip, port=broker_port, keepalive=60)
            request = create_upload_request(to, contents)
            client.publish(pub_topic, request)
            client.disconnect()

        except:
            print('送信失敗')

        sleep(measure_interval_sec)

except KeyboardInterrupt:
    irgw.close()
    client.disconnect()
