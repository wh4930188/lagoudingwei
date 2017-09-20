#!/usr/bin/python3
import queue
import threading
import uuid
     #引入各类 接口
from BaiduMapAPI import BaiduMapAPI
from LagouAPI import LagouAPI
from JobDB import db, Job
import settings

db.create_all()
jq = queue.Queue()   #队列
lock = threading.Lock()  #线程锁
done = False   #一个flag

     #定义爬取函数
def geo_worker():
    while True:
        try:
            jd = jq.get(timeout=1)
        except queue.Empty:
            with lock:
                if done:
                    break
            continue
        address = LagouAPI.get_location_by_pos_id(jd['positionId'])  #调用接口,写入参数
        gis = BaiduMapAPI.search(settings.CITY, address)  #调用地图API,写入搜索的地点名称
        job = Job(str(uuid.uuid1()))   #数据库相关操作
        job.company_name = jd['companyFullName']
        job.location = address     #工作地址
        job.ctime = jd['createTime']   #工作的创建时间
        job.salary = jd['salary']     #工资的薪资
        job.company_size = jd['companySize']   #公司人数大小
        job.field = jd['industryField']
        job.stage = jd['financeStage']
        job.title = jd['positionName']    #职位名称
        job.jid = jd['positionId']     #职位id

        if gis:
            print(gis)
            try:
                loc = gis[0]['location']
                job.lat, job.lng = loc['lat'], loc['lng']
                if 'address' in gis[0]:
                    job.gis_loc = gis[0]['address']
            except Exception:
                pass

        db.session.add(job)
        print('正在保存',job.title)
        db.session.commit()
        print('保存成功',job.title)

geo_thread = threading.Thread(target=geo_worker)
geo_thread.start()


def main():
    global done     #将标记为全局化

    try:
        for jd in LagouAPI.search(settings.KEYWORDS, city=settings.CITY):
            jq.put(jd)   #在职位搜索API中设置,所需要的参数,将拿到的值放到队列中
        with lock:
            done = True    #更换标志位
        geo_thread.join()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

