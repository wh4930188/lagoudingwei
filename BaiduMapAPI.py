import functools
import hashlib
import time
import urllib.parse

import requests


class BaiduMapAPI(object):
    BAIDU_GATEWAY = 'http://api.map.baidu.com'
    BAIDU_API_KEY = 'dau166fzWo0E63ZcRVwHyvDn'
    BAIDU_API_SK = 'V1CAa3lYgARGAioGqhUaNhhW4m1Fz8sw'
    sess = requests.Session()

    @classmethod
    @functools.lru_cache(65536)    #一个缓存机制的函数
    def search(cls, city, loc):   #定义一个类的搜索方法
        q = '/place/v2/search?ak=%s&q=%s&region=%s&output=json&timestamp=%d' % (
            cls.BAIDU_API_KEY, loc, city, time.time())   #这是接口后的内容
        encoded_str = urllib.parse.quote(q, safe="/:=&?#+!$,;'@()*[]")
        raw_str = encoded_str + cls.BAIDU_API_SK
        sn = hashlib.md5(urllib.parse.quote_plus(raw_str).encode('UTF-8')).hexdigest()
        ret = cls.sess.get(cls.BAIDU_GATEWAY + q + '&sn=' + sn).json()
        if ret['status'] == 0:
            return ret['results']
        return None
