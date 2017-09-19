from bs4 import BeautifulSoup
import requests
# url='https://www.lagou.com/jobs/3251480.html'
# headers = {
#      'Cookie': 'SESSIONID=ABAAABAAAIAACBI386BBF2A4AF17A015A35A443275F849E; user_trace_token=20170823222931-7a66d0be-880f-11e7-8e7c-5254005c3644; LGUID=20170823222931-7a66d82d-880f-11e7-8e7c-5254005c3644; X_HTTP_TOKEN=efbd926a2120df44637a9a572dfe0f6e; _putrc=8582F8EBD102AF67; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B71976; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; TG-TRACK-CODE=search_code; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503498572; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1503502613; _ga=GA1.2.1002397109.1503498572; _gid=GA1.2.1028357858.1503498572; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fpx%3Ddefault%26xl%3D%25E6%259C%25AC%25E7%25A7%2591%26city%3D%25E5%258C%2597%25E4%25BA%25AC; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fpx%3Ddefault%26city%3D%25E5%258C%2597%25E4%25BA%25AC; LGSID=20170823233652-e3035a6a-8818-11e7-9fe3-525400f775ce; LGRID=20170823233656-e535491c-8818-11e7-9fe3-525400f775ce; SEARCH_ID=cc7603ed348d42898fdaec6b2dcb5e23; index_location_city=%E5%85%A8%E5%9B%BD',
#      "Host": "www.lagou.com",
#      "Origin": "https://www.lagou.com",
#      "Referer": "https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=",
#      "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
#      "X-Anit-Forge-Code": "0",
#      "X-Anit-Forge-Token": "None",
#      "X-Requested-With": "XMLHttpRequest",
# }
#
# html=requests.get(url,headers=headers).text
# soup=BeautifulSoup(html,"lxml")
# addrs=soup.select(".work_addr")[0]
# print(addrs.text.replace(" ","").replace("\n","")[:-4])
# for i in addrs:
#      print(i)
proxy_get=requests.get("http://127.0.0.1:5000/get").text
print(proxy_get)