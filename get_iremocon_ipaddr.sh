#!/bin/bash
sudo arp-scan -I wlan0 -l | grep Wiznet | awk '{print $1}'



