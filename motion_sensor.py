#!/usr/bin/env python
#-*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO

class HumanDetector(object):

  CHECK_INTERVAL_SEC = 3
  TIME_NEEDED_JUDGE_ABSENCE = 10
  SENSOR_PIN = 18
  
  def __init__(self):
#    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.SENSOR_PIN, GPIO.IN)
    self.motion_detected = False
    self.undetected_time = 0

  def monitor(self, on_detected, on_undetected):

    while True:
      if(GPIO.input(self.SENSOR_PIN) == GPIO.HIGH):
        self.undetected_time = 0

      if(GPIO.input(self.SENSOR_PIN) == GPIO.HIGH) and (self.motion_detected == False):
        self.motion_detected = True
        on_detected()

      sleep(self.CHECK_INTERVAL_SEC)

      self.undetected_time += self.CHECK_INTERVAL_SEC

      if(self.undetected_time >= self.TIME_NEEDED_JUDGE_ABSENCE) and (self.motion_detected == True):
        self.motion_detected = False
        on_undetected()
