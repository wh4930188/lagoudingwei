import urllib.parse

import requests
import time
from bs4 import BeautifulSoup

#到这里就应该是对  拉钩的API进行爬取
class LagouAPI(object):   #定义了一个拉钩的类\?
    LAGOU_GATEWAY = 'https://www.lagou.com/jobs/positionAjax.json?'   #写入一个API地址
    sess = requests.Session()   #建立一个会话
    headers = {
        'Cookie': 'SESSIONID=ABAAABAAAIAACBI386BBF2A4AF17A015A35A443275F849E; user_trace_token=20170823222931-7a66d0be-880f-11e7-8e7c-5254005c3644; LGUID=20170823222931-7a66d82d-880f-11e7-8e7c-5254005c3644; X_HTTP_TOKEN=efbd926a2120df44637a9a572dfe0f6e; _putrc=8582F8EBD102AF67; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B71976; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; TG-TRACK-CODE=search_code; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503498572; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503502613; _ga=GA1.2.1002397109.1503498572; _gid=GA1.2.1028357858.1503498572; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fpx%3Ddefault%26xl%3D%25E6%259C%25AC%25E7%25A7%2591%26city%3D%25E5%258C%2597%25E4%25BA%25AC; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fpx%3Ddefault%26city%3D%25E5%258C%2597%25E4%25BA%25AC; LGSID=20170823233652-e3035a6a-8818-11e7-9fe3-525400f775ce; LGRID=20170823233656-e535491c-8818-11e7-9fe3-525400f775ce; SEARCH_ID=cc7603ed348d42898fdaec6b2dcb5e23; index_location_city=%E5%85%A8%E5%9B%BD',
        "Host": "www.lagou.com",
        "Origin": "https://www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
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
            time.sleep(20)        #---------------------------------------------------------------------延迟
            r = requests.post(cls.jl_url,headers=cls.headers,data=data)   #实用会话请求

            # 对返回的结果进行JSON序列化
            json_result = r.json()
            print(json_result)
            if page_max is None:
                # 获得页数
                # page_max = json_result['content']['totalPageCount']
                # 拉钩返回的数据比之前多了一层'positionResult'，并且字段名也由totalPageCount变为totalCount
                # print(json_result['content']['positionResult']['totalCount'])
                page_max=json_result['content']['positionResult']['totalCount']//15
                # print(page_max)
                # page_max = json_result['content']['positionResult']['totalCount']
            # 用生成器返回得到的结果
            # for j in json_result['content']['result']:
            # 拉钩返回的数据比之前多了一层'positionResult'
            for j in json_result['content']['positionResult']['result']:
                yield j
            if page >= page_max:
                break
            else:
                data['first']='false'
            page += 1

    @classmethod
    def get_location_by_pos_id(cls, pos_id):
        time.sleep(15)
        url='https://www.lagou.com/jobs/%d.html' % pos_id
        print('正在收集数据:',url)
        try:
            proxy_get = requests.get("http://127.0.0.1:5000/get").text
            print(proxy_get)
            proxies = {
                "http": "http://%s" % proxy_get,
            }
            r = requests.get(url,headers=LagouAPI.headers,proxies=proxies)
            soup = BeautifulSoup(r.text, 'html.parser')
            addrs = soup.select(".work_addr")[0]
        except Exception as e:
            print(e)
            cls.get_location_by_pos_id(pos_id)
        else:
            addr=addrs.text.replace(" ", "").replace("\n", "")[:-4]
            print(addr)
            return addr     #暂时不知道是干啥的,推测是获取地址的

