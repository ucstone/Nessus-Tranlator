#/usr/bin/env python
#coding=utf8
 
import httplib
import md5
import urllib
import random
import json
import ConfigParser
import os


def translate(q_word=None):
    # config_path = os.path.join(os.path.dirname(__file__), "baidu_api.conf")
    config_path = r"c:\\baidu_api.conf"
    cfg = ConfigParser.ConfigParser()
    cfg.read(config_path)
    # 获取IP信息
    api_dict = dict(cfg.items('BAIDU_API'))
    # print api_dict
    appid = api_dict['appid']
    secretKey = api_dict['secretkey']
    # print appid, secretKey


    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = q_word
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        # print response.read()
        res = json.load(response)
        xx = res['trans_result'][0]['dst']
        return xx
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()


# if __name__ == "__main__":
#     translate()