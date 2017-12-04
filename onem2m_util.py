#-*- coding: utf-8 -*-
import string
import random
import json
from datetime import datetime


def create_upload_request(str_to, str_content):
    request_template = \
        '{{"op":1,"to":"{0}","fr":"IN-AE-ID","rqi":"{1}","ty":4,"pc":{{"m2m:cin":{{"ty": 4,"cnf": "text/plain:0","con":"{2}"}}}}}}'
    request_id = __get_request_id()
    return request_template.format(str_to, request_id, str_content)

def extract_notify_cin_con(str_json_notify_req):
    try:
        notification = json.loads(str_json_notify_req)
        str_representation = notification['pc']['m2m:sgn']['nev']['rep']
        representation = json.loads(str_representation)
        content = representation['m2m:cin']['con']
        return content

    except ValueError as e:
        print('{}'.format(e.args))
        return None

    except KeyError as e:
        print('{}'.format(e.args))
        return None

def __get_request_id():
    chara_num = 5
    random_str = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(chara_num)])
    request_id = datetime.now().strftime("%Y%m%d%H%M%S") + random_str
    return request_id
