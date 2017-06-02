#-*- coding: utf-8 -*-
import string
import random
from datetime import datetime


def create_upload_request(str_to, str_content):
    request_template = \
        '{{"op":1,"to":"{0}","fr":"IN-AE-ID","rqi":"{1}","ty":4,"pc":{{"m2m:cin":{{"con":"{2}"}}}}}}'
    request_id = __get_request_id()
    return request_template.format(str_to, request_id, str_content)


def __get_request_id():
    chara_num = 5
    random_str = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(chara_num)])
    request_id = datetime.now().strftime("%Y%m%d%H%M%S") + random_str
    return request_id
