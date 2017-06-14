#-*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import config
from onem2m_util import create_upload_request


class MotionSensor(object):

    SENSOR_PIN = 18

    def __init__(self, check_interval, time_to_judge_absence):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN, GPIO.IN)
        self._motion_detected = False
        self._undetected_time = 0
        self._check_interval = check_interval
        self._time_to_judge_absence = time_to_judge_absence

    def monitor(self, on_detected, on_undetected):
        while True:
            if(GPIO.input(self.SENSOR_PIN) == GPIO.HIGH):
                self._undetected_time = 0

            if(GPIO.input(self.SENSOR_PIN) == GPIO.HIGH) and (self._motion_detected == False):
                self._motion_detected = True
                on_detected()

            sleep(self._check_interval)

            self._undetected_time += self._check_interval

            if(self._undetected_time >= self._time_to_judge_absence) and (self._motion_detected == True):
                self._motion_detected = False
                on_undetected()


def __on_detected():
    print('人を感知しました')
    try:
        client.connect(broker_ip, port=broker_port, keepalive=60)
        request = create_upload_request(to, '1')
        client.publish(pub_topic, request)
        client.disconnect()
    except:
        print('送信失敗')

def __on_undetected():
    print('人がいなくなりました')
    try:
        client.connect(broker_ip, port=broker_port, keepalive=60)
        request = create_upload_request(to, '0')
        client.publish(pub_topic, request)
        client.disconnect()
    except:
        print('送信失敗')


if __name__ == '__main__':
    broker_ip = config.get('mqtt_broker', 'ip')
    broker_port = config.getint('mqtt_broker', 'port')

    pub_topic = config.get('mqtt_client', 'pub_topic')
    client_id = config.get('mqtt_client', 'client_id')

    to = config.get('container_uri', 'motion_sensor_data')

    check_interval_sec = config.getint('motion_sensor', 'check_interval_sec')
    time_to_judge_absence_sec = config.getint('motion_sensor', 'time_to_judge_absence_sec')

    client = mqtt.Client(client_id=client_id, clean_session=False, protocol=mqtt.MQTTv311)

    try:
        m_sensor = MotionSensor(check_interval_sec, time_to_judge_absence_sec)
        m_sensor.monitor(__on_detected, __on_undetected)

    finally:
        client.disconnect()
