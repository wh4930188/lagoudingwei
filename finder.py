#!/usr/bin/python3
import queue
import threading
import uuid
     #引入各类 接口
from BaiduMapAPI import BaiduMapAPI
from LagouAPI import LagouAPI
from JobDB import db, Job

jq = queue.Queue()   #队列
lock = threading.Lock()  #线程锁
done = False   #一个flag

     #定义爬取函数
def geo_worker():
    while True:
        try:
            jd = jq.get(timeout=1)       #从队列中获取,大概是一个url
        except queue.Empty:  #如果队列为空
            with lock:   #释放锁
                if done:   #如果完成队列的取得? 那就中断循环
                    break
            continue
        address = LagouAPI.get_location_by_pos_id(jd['positionId'])  #调用接口,写入参数
        gis = BaiduMapAPI.search('深圳', address)  #调用地图API,写入搜索的地点名称
        print(gis)
        job = Job(str(uuid.uuid1()))   #数据库相关操作
        job.company_name = jd['companyFullName']#----------------以下设置各类字段
        job.location = address     #工作地址
        job.ctime = jd['createTime']   #工作的创建时间
        job.salary = jd['salary']     #工资的薪资
        job.company_size = jd['companySize']   #公司人数大小
        job.field = jd['industryField']   #我也不知道是傻
        job.stage = jd['financeStage']
        job.title = jd['positionName']    #职位名称
        job.jid = jd['positionId']     #职位id

        if gis:          #地图的一个创建?!??!???????????
            print(gis)
            try:
                loc = gis[0]['location']          #不知道取的什么
                job.lat, job.lng = loc['lat'], loc['lng']
                if 'address' in gis[0]:
                    job.gis_loc = gis[0]['address']
            except Exception:
                pass

        db.session.add(job)        #保持了一个什么会话?
        db.session.commit()

geo_thread = threading.Thread(target=geo_worker)    #创建了一个线程.去执行?爬取任务
geo_thread.start()


def main():
    global done     #将标记为全局化
    try:
        for jd in LagouAPI.search('Python爬虫', city='深圳'):
            jq.put(jd)   #在职位搜索API中设置,所需要的参数,将拿到的值放到队列中
        with lock:              #锁住?  守护进程??
            done = True    #更换标志位
        geo_thread.join()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

