# /usr/bin/env python
# coding=utf8

import requests
import hashlib
from urllib.parse import quote
import time
import json
from log import error, info


def translate(q_word=None):
    # 申请百度翻译API
    appid = ""
    secretKey = ""

    baidu_url = '/api/trans/vip/translate'
    q = q_word
    fromLang = 'en'
    toLang = 'zh'
    salt = int(time.time())

    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    baidu_data = baidu_url + '?appid=' + appid + '&q=' + quote(
        q_word) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        req = requests.get(url="https://api.fanyi.baidu.com"+baidu_data)
        # info(req.text)
        print(req.text)
        trans_result = json.loads(req.text)
        xx = trans_result['trans_result']
        # info(xx)

        if len(xx) == 1:
            info(xx[0]['dst'])
            return xx[0]['dst']
        else:
            res = ''
            for dst in xx:
                # info(dst)
                res = res + dst['dst']
            info(res)
            return res
    except Exception as e:

        error(e)


if __name__ == "__main__":
    translate('Hello World')
