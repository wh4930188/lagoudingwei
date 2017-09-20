# from bs4 import BeautifulSoup
# import requests
# import urllib.parse
# import queue
# q=queue.Queue()
#
# # city=input('请输入城市名称:')
#
#
# key={
# 'city':'深圳'
# }
# city_code=urllib.parse.urlencode(key)
# url='https://www.lagou.com/jobs/positionAjax.json?px=default&{0}&needAddtionalResult=false&isSchoolJob=0'.format(city_code)
#     # 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false&isSchoolJob=0'
# print(url)
# data={
# 'first':'true',
# 'pn':1,
# 'kd':'python'
# }
# headers={
# "Accept":"application/json, text/javascript, */*; q=0.01",
# "Accept-Encoding":"gzip, deflate, br",
# "Accept-Language":"zh-CN,zh;q=0.8",
# "Connection":"keep-alive",
# "Content-Length":"25",
# "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
# "Cookie":"user_trace_token=20170720161947-8c452fdc-d715-4bb0-93b6-6ed1316fcc17; LGUID=20170720161950-336b05fd-6d24-11e7-b273-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=3ea16b008ded24e113fe53afcbad6624; JSESSIONID=ABAAABAACEBACDGC785B415D96C39AEEF4E53B2425D1EFE; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=search_code; _gid=GA1.2.2069330153.1505813531; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504002248,1505458603,1505813531,1505892945; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505903840; _ga=GA1.2.1635684239.1500538789; LGSID=20170920181323-55c716de-9dec-11e7-9c27-525400f775ce; LGRID=20170920183723-b060430e-9def-11e7-91f0-5254005c3644; SEARCH_ID=ec7efa8213204756b0a64c4ecb4a55b7",
# "Host":"www.lagou.com",
# "Origin":"https://www.lagou.com",
# "Referer":"https://www.lagou.com/jobs/list_python?px=default&city=%E6%B7%B1%E5%9C%B3",
# "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
# "X-Anit-Forge-Code":"0",
# "X-Anit-Forge-Token":"None",
# "X-Requested-With":"XMLHttpRequest",
# }
# response=requests.post(url,data=data,headers=headers)
# print(response.json())
# totalCount=response.json()['content']['positionResult']['totalCount']
# pagemax,_=divmod(totalCount,15)
# pagemax+=1
# print(pagemax)
# urls=[]
# for page in range(1,pagemax+1):
#     if page!=1:
#         data['first'] = 'false'
#         data['pn']=page
#     print(data)
#     response = requests.post(url, data=data, headers=headers)
#     print(response.json())
#     results=response.json()['content']['positionResult']['result']
#     for item in results:
#         # print(item['positionId'])
#         posid=item['positionId']
#         urls.append(posid)
# f=open('a.txt','a+')
# for i in urls:
#     f.write(str(i)+'\n')
#
#
#
# f=open('a.txt','r')
# for line in f:
#     id=line.strip("\n")
#     url='https://www.lagou.com/jobs/%s.html'%(id)
#     # print(url)
#
#     headers={
#         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "Accept-Encoding":"gzip, deflate, br",
#         "Accept-Language":"zh-CN,zh;q=0.8",
#         "Cache-Control":"max-age=0",
#         "Connection":"keep-alive",
#         "Cookie":"user_trace_token=20170720161947-8c452fdc-d715-4bb0-93b6-6ed1316fcc17; LGUID=20170720161950-336b05fd-6d24-11e7-b273-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=3ea16b008ded24e113fe53afcbad6624; JSESSIONID=ABAAABAACEBACDGC785B415D96C39AEEF4E53B2425D1EFE; TG-TRACK-CODE=search_code; SEARCH_ID=352241e735d94ee1aaa22241ef1f8743; _gid=GA1.2.2069330153.1505813531; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504002248,1505458603,1505813531,1505892945; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1505906123; _ga=GA1.2.1635684239.1500538789; LGSID=20170920181323-55c716de-9dec-11e7-9c27-525400f775ce; LGRID=20170920191527-012815a4-9df5-11e7-9c31-525400f775ce",
#         "Host":"www.lagou.com",
#         "Upgrade-Insecure-Requests":"1",
#         "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
#     }
#     try:
#         response=requests.get(url,headers=headers,timeout=10)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         addrs = soup.select(".work_addr")[0]
#     except Exception as e:
#         print(e)
#     else:
#         addr=addrs.text.replace(" ", "").replace("\n", "")[:-4]
#         print(addr)
#
#
from flask import Flask, render_template, jsonify
from JobDB import Job
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sqlite.data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Job(
    id = 'asdasd'
    title = db.Column(db.String(40))
    company_name = db.Column(db.String(128))
    location = db.Column(db.String(128))
    ctime = db.Column(db.Integer)
    salary = db.Column(db.String(40))
    field = db.Column(db.String(40))
    company_size = db.Column(db.String(40))
    stage = db.Column(db.String(40))
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    gis_loc = db.Column(db.String(128))
    jid = db.Column(db.Integer)
)