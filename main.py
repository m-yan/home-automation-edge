#!/usr/bin/env python
#-*- coding: utf-8 -*-

import motion_sensor 


def on_detected():
  print("人を感知しました")

def on_undetected():
  print("人がいなくなりました")

a = motion_sensor.HumanDetector();

a.monitor(on_detected, on_undetected)
