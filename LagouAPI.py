import urllib.parse

import requests
import time
from bs4 import BeautifulSoup

#到这里就应该是对  拉钩的API进行爬取
class LagouAPI(object):   #定义了一个拉钩的类\?
    LAGOU_GATEWAY = 'https://www.lagou.com/jobs/positionAjax.json?'   #写入一个API地址

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": "25",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "user_trace_token=20170720161947-8c452fdc-d715-4bb0-93b6-6ed1316fcc17; LGUID=20170720161950-336b05fd-6d24-11e7-b273-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=3ea16b008ded24e113fe53afcbad6624; JSESSIONID=ABAAABAACEBACDGC785B415D96C39AEEF4E53B2425D1EFE; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=search_code; _gid=GA1.2.2069330153.1505813531; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504002248,1505458603,1505813531,1505892945; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505903840; _ga=GA1.2.1635684239.1500538789; LGSID=20170920181323-55c716de-9dec-11e7-9c27-525400f775ce; LGRID=20170920183723-b060430e-9def-11e7-91f0-5254005c3644; SEARCH_ID=ec7efa8213204756b0a64c4ecb4a55b7",
        "Host": "www.lagou.com",
        "Origin": "https://www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_python?px=default&city=%E6%B7%B1%E5%9C%B3",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        "X-Anit-Forge-Code": "0",
        "X-Anit-Forge-Token": "None",
        "X-Requested-With": "XMLHttpRequest",
    }
    @classmethod    #创建一个类方法   ,关于搜索的
    def search(cls, kd, **kwargs):
        """
        :param kd: 关键字
        :param kwargs: 其他参数
        :return:
        """
        # 对url参数进行编码
        url_encoded = urllib.parse.urlencode(kwargs,)     #将输入的参数encode
        print(url_encoded)
        # 拼接url
        # cls.jl_url = cls.LAGOU_GATEWAY + url_encoded     #encode的结果路径拼接
        cls.jl_url='https://www.lagou.com/jobs/positionAjax.json?px=default&{0}&needAddtionalResult=false&isSchoolJob=0'.format(url_encoded)
        print(cls.jl_url)
        page = 1
        page_max = None
        while True:     #这是传入的参数
            data = {
                'first': 'true',
                'pn': page,
                'kd': kd
            }
            print(data)
            # 请求结果
            r = requests.post(cls.jl_url,headers=cls.headers,data=data)   #实用会话请求
            # 对返回的结果进行JSON序列化
            json_result = r.json()
            print(json_result)
            if page_max is None:
                totalCount = json_result['content']['positionResult']['totalCount']
                page_max, _ = divmod(totalCount, 15)
                page_max += 1
            for j in json_result['content']['positionResult']['result']:
                yield j
            if page >= page_max:
                break
            else:
                data['first']='false'
            page += 1

    @classmethod
    def get_location_by_pos_id(cls, pos_id):
        url='https://www.lagou.com/jobs/%d.html' % pos_id
        print('正在收集数据:',url)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "user_trace_token=20170720161947-8c452fdc-d715-4bb0-93b6-6ed1316fcc17; LGUID=20170720161950-336b05fd-6d24-11e7-b273-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=3ea16b008ded24e113fe53afcbad6624; JSESSIONID=ABAAABAACEBACDGC785B415D96C39AEEF4E53B2425D1EFE; TG-TRACK-CODE=search_code; SEARCH_ID=352241e735d94ee1aaa22241ef1f8743; _gid=GA1.2.2069330153.1505813531; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504002248,1505458603,1505813531,1505892945; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505906123; _ga=GA1.2.1635684239.1500538789; LGSID=20170920181323-55c716de-9dec-11e7-9c27-525400f775ce; LGRID=20170920191527-012815a4-9df5-11e7-9c31-525400f775ce",
            "Host": "www.lagou.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            addrs = soup.select(".work_addr")[0]
        except Exception as e:
            print(e)
        else:
            addr = addrs.text.replace(" ", "").replace("\n", "")[:-4]
            print(addr)
            return addr
