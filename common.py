#-*- coding: utf-8 -*-
import socket
import config
import re

class IRemoconGW(object):
    def __init__(self):
        self._iremocon_ip = config.get('iremocon', 'ip')
        self._iremocon_port = config.getint('iremocon', 'port')
        self._sock = self.__get_iremocon_connection()
        self._pattern = re.compile('\w+;ok;(.+)\r\n')


    def send_command(self, str_command):
        if str_command is None:
            return

        try:
            self._sock.send(str_command.encode('utf-8') + b'\r\n')
            print('Command {} sended.'.format(str_command))
            print(self._sock.recv(4096))

        except socket.error:
            self._sock.close()
            self._sock = __get_iremocon_connection()


    def get_temperature(self):
        try:
            self._sock.send(b'*te\r\n')
            response = self._sock.recv(4096).decode('utf-8')
            temperature = self._pattern.search(response).group(1)
            return round(float(temperature), 1)

        except socket.error:
            self._sock.close()
            self._sock = __get_iremocon_connection()


    def get_humidity(self):
        try:
            self._sock.send(b'*hu\r\n')
            response = self._sock.recv(4096).decode('utf-8')
            humidity = self._pattern.search(response).group(1)
            return int(float(humidity))

        except socket.error:
            self._sock.close()
            self._sock = __get_iremocon_connection()


    def get_illuminance(self):
        try:
            self._sock.send(b'*li\r\n')
            response = self._sock.recv(4096).decode('utf-8')
            illuminance = self._pattern.search(response).group(1)
            return int(float(illuminance))

        except socket.error:
            self._sock.close()
            self._sock = __get_iremocon_connection()


    def close(self):
        self._sock.close()
        print('Connection to iRemocon closed.')


    def __get_iremocon_connection(self):
        sock = socket.create_connection((self._iremocon_ip, self._iremocon_port), timeout=5)
        print('Connected sucessfully to iRemocon.')
        sock.settimeout(None)
        return sock
