#-*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import socket
import config
import json

def on_connect(client, sock, flags, rc):
    client.subscribe(sub_topic)


def on_message(client, sock, message):
    str_payload = message.payload.decode('utf-8')
    print(message.topic + ' ' + str_payload)

    iremocon_command = extract_notify_cin_con(str_payload)
    if iremocon_command is None:
        return

    try:
        sock.send(iremocon_command.encode('utf-8') + b'\r\n')
        print('Command {} sended.'.format(iremocon_command))
        print(sock.recv(4096))
    
    except socket.error:
        sock.close()
        sock = get_iremocon_connection()
        self.user_data_set(sock)


def on_disconnect(client, sock, rc):
    sock.close()
    print('Connection to iRemocon closed.')


def get_iremocon_connection():
    sock = socket.create_connection((iremocon_ip, iremocon_port), timeout=5)
    print('Connected sucessfully to iRemocon.')
    sock.settimeout(None)
    return sock


def extract_notify_cin_con(str_json_notify_req):
    try:
        req = json.loads(str_json_notify_req)
        content = req['pc']['m2m:cin']['con']
        return content
    
    except ValueError as e:
        print('{}'.format(e.args))
        return None
    
    except KeyError as e:
        print('{}'.format(e.args))
        return None


if __name__ == '__main__':
    broker_ip = config.get('mqtt_broker', 'ip')
    broker_port = config.getint('mqtt_broker', 'port')
    sub_topic = config.get('mqtt_client', 'sub_topic')
    
    iremocon_ip = config.get('iremocon', 'ip')
    iremocon_port = config.getint('iremocon', 'port')
    
    try:
        sock = get_iremocon_connection()
        
        client = mqtt.Client(protocol=mqtt.MQTTv311, userdata=sock)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        
        client.connect(broker_ip, port=broker_port, keepalive=60)
        print('Connected sucessfully to MQTT Broker.')
        
        client.loop_forever()
        
    finally:
        client.disconnect()
        print('Connection to MQTT Broker closed.')
