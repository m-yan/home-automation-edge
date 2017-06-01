#-*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt


class MotionSensor(object):

    SENSOR_PIN = 18

    def __init__(self, check_interval, time_to_judge_absence):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN, GPIO.IN)
        self.motion_detected = False
        self.undetected_time = 0
        self.check_interval = check_interval
        self.time_to_judge_absence = time_to_judge_absence

    def monitor(self, on_detected, on_undetected):
        while True:
            if(GPIO.input(self.SENSOR_PIN) == GPIO.HIGH):
                self.undetected_time = 0

            if(GPIO.input(self.SENSOR_PIN) == GPIO.HIGH) and (self.motion_detected == False):
                self.motion_detected = True
                on_detected()

            sleep(self.check_interval)

            self.undetected_time += self.check_interval

            if(self.undetected_time >= self.time_to_judge_absence) and (self.motion_detected == True):
                self.motion_detected = False
                on_undetected()

# 人感センサの値のチェック間隔
CHECK_INTERVAL_SEC = 3
# 何秒間検知しなければ不在として判断するか
TIME_TO_JUDGE_ABSENCE_SEC = 30
MQTT_BROKER = '13.78.50.153'
MQTT_BROKER_PORT = 1883
MQTT_CLIENT_ID = 'AE:ASN-AE'
PUB_TOPIC = 'oneM2M/req/ADN-AE/IN-CSE/json'

def on_detected():
    print("人を感知しました")
    client.connect(MQTT_BROKER, port=MQTT_BROKER_PORT, keepalive=60)
    client.publish(PUB_TOPIC, '1')
    client.disconnect()

def on_undetected():
    print("人がいなくなりました")
    client.connect(MQTT_BROKER, port=MQTT_BROKER_PORT, keepalive=60)
    client.publish(PUB_TOPIC, '0')
    client.disconnect()

if __name__ == '__main__':
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=False, protocol=mqtt.MQTTv311)

    try:
        m_sensor = MotionSensor(CHECK_INTERVAL_SEC, TIME_TO_JUDGE_ABSENCE_SEC)
        m_sensor.monitor(on_detected, on_undetected)

    except KeyboardInterrupt:
        client.disconnect()
