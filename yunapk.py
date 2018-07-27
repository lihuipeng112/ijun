# -*- coding:utf-8 -*- 

import sys
import os
import os.path
from time import sleep
import time
import threading 
import pymysql
import random
import unittest
import string
import platform
from subprocess import Popen, PIPE
import requests
import datetime
import importlib

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
importlib.reload(sys)


game=""
game_id=""
channel=""
channel_id=""
url=""
apk=""
task_id=""
f1=""
ip="192.168.1.230"

def cmdrun(command):
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    out += err
    return out

def download():
    global f1
    # path="/home/work/yuntest/share_apks/"+game_id+"/"+apk
    # if os.path.isfile(path):
    #     f1=path
    #     returns
    print("downloading with requests")
    t1=datetime.datetime.now()
    #url = 'http://res.youyunad.com/cloud_pack/outputs/qmmd/qmmd_agent_qihu_1_2.0.9_20160513_2219.apk' 
    r = requests.get(url)
    f1="/home/work/yuntest/apks/"+apk
    with open(f1, "wb") as code:
         code.write(r.content)
    # 针对游戏下载不完整问题进行优化
    k=0
    while os.path.getsize(f1) / 1024 / 1024 < 100 and k <3:
        os.popen('rm -rf ' + f1)
        r = requests.get(url)
        with open(f1, "wb") as code:
            code.write(r.content)
        k=k+1
    t2=datetime.datetime.now()
    print("下载用时："+str((t2-t1).seconds))
    t = threading.Thread(target=copyapk)
    t.start()
    
    return
def copyapk():
    #检查task目录
    apk_dir="/home/work/yuntest/server/yunapk/"+game_id
    apk_dir="/home/work/yuntest/share_apks/"+game_id
    if not os.path.isdir(apk_dir):
        os.system("mkdir "+apk_dir)
    apk_dir=apk_dir+"/"
    print("把apk复制到云测服务器")
    os.popen("\cp -rf "+f1+" "+apk_dir)
    return
def getpackageinfo():
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    napk=f1
    pac=cmdrun("aapt dump badging " + napk + " | grep package")
    print(pac)
    #(a,package,b,version_code,d,version,e,f,g)=pac.split("'")
    pa=pac.split("'")
    package=pa[1]
    version_code=pa[3]
    version=pa[5]
    print(package+" "+version)
    if package=="":
        sql="update task set a_state='失败'，comments='apk解析失败' where apk='"+apk+"'"
        print("包解析失败")
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return
    pac=cmdrun("aapt dump badging " + napk + " | grep application-label:")
    #(a,game,b)=pac.split("'")
    game=pac.split("'")[1]
    pac=cmdrun("aapt dump badging " + napk + " | grep launchable-activity")
    print(pac)
    #(a,activity,b,c,d,e,f)=pac.split("'")
    activity=pac.split("'")[1]
    packageinfo=game+" "+package+" "+version
    sql="update task set package='"+package+"',activity='"+activity+"',packageinfo='"+packageinfo+"',version_code='"+version_code+"',game='"+game+"' where apk='"+apk+"'"
    print(sql)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return
def addtask():
    global game
    global game_id
    global apk
    global url
    global channel
    global channel_id
    global task_id
    game=""
    channel=""
    url=""
    apk=""
    task_id=""
    game_id=""
    channel_id=""
    game_exe=""
    channel_script=""
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    sql="select task_id,game,channel,url from yunapk where channel in ('199') and state=1 order by id limit 1"
    sql="select y.task_id,y.game,y.channel,y.url from yunapk y,xuqiu_list l,xuqiu x where y.state=1 and y.task_id=l.d_task_id and l.xuqiu_id=x.id and x.state=1 and y.download=2 order by y.id limit 1"
    cur.execute(sql)
    for each in cur:        
        (task_id,game,channel,url)=each
    if url=="":
        sql="update yunapk set state=0,comments='下载地址为空' where task_id='"+task_id+"'"
        print("无出包需求，结束")
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        sleep(30)
        return
    apks=url.split("/")
    apk=apks[-1]
    print("apk is :"+apk)
    #获取其他信息
    sql="select game_id,game_exe from game where id='"+game+"'"
    cur.execute(sql)
    
    for each in cur:
        (game_id,game_exe)=each
    print("game_exe,"+game_exe)
    sql="select channel_id,channel_script from channel where id='"+channel+"'"
    cur.execute(sql)
    for each in cur:
        (channel_id,channel_script)=each
    '''
    if channel_id.find("ysdkjh")>-1:
        channel_script="yingyongbao.py"
    if channel_id.find("jh37jh")>-1:
        channel_script="37wan.py"
    if channel_id.find("shoumengjh")>-1:
        channel_script="shoumeng.py"
    '''
    print("channel_script"+channel_script)
    #获取apk信息
    gamepy="/home/work/yuntest/python/"+game_id+".py"
    if not os.path.isfile(gamepy) :
        print("缺渠道或者游戏脚本，不增加测试任务，返回。")
        sql="update yunapk set state=0,comments='无游戏脚本' where task_id='"+task_id+"'"
        #print("下载地址为空")
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return
    if channel_script.find(".py")==-1 :
        print("缺渠道或者游戏脚本，不增加测试任务，返回。")
        sql="update yunapk set state=0,comments='无渠道脚本' where task_id='"+task_id+"'"
        #print("下载地址为空")
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return
    #检查是否有发包，有发过包才送云测  

    fb=0
    description=""
    sql="select count(*) from fabao f,yunapk y ,game g where f.game_id =g.game_id and y.game=g.id and y.channel=f.channel_id1 and y.task_id='"+task_id+"' and f.game_channel_id=y.game_channel_id"
    #game>62,的游戏取 game_channel_id
    if int(game)>62:
        sql="select count(*),y.description from fabao f,yunapk y ,game g where f.game_id =g.game_id and y.game=g.id and y.channel=f.channel_id1 and y.task_id='"+task_id+"' and f.game_channel_id=y.game_channel_id and f.type='正式'"
    else:
        sql="select count(*),y.description from fabao f,yunapk y ,game g where f.game_id =g.game_id and y.game=g.id and y.channel=f.channel_id1 and y.task_id='"+task_id+"' and f.type='正式'"
    cur.execute(sql)
    for each in cur:        
        (fb,description)=each
    #应用宝分包、子包，直接送测。需要从业务上进行规范，主包测试通过后再提测分包
    if channel=="10029" or channel=="177" or channel=="78":
        if description.find("分包")>-1 or description.find("子包")>-1:
            fb=1
    if fb==0:
        print("首次发包，不增加测试任务，返回。")
        sql="update yunapk set state=0,comments='首次发包，不送测' where task_id='"+task_id+"'"
        #print("下载地址为空")
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return      
    
    #为规避安装失败问题，不下载        
    #download()
    #若共享上无文件，返回。
    global f1
    f1="/home/work/yuntest/share_apks/"+game_id+"/"+apk
    if not os.path.isfile(f1):
        print("共享上无文件，等会再加任务"+f1)
        sleep(10)
        return  
        

    #加执行任务
    url1 = "http://192.168.1.204:8080/addtask.jsp"
    #初始化device
    device="df22ca99"
    #查询任务少的设备，获取后处理
    sql="select device from task where device in (select device from device where isauto1=1) and a_state in ('allagain','new') group by device order by count(*) limit 1"
    sql="select d.device from device d right join task t on d.isauto1=1 and d.device=t.device and t.a_state in ('new','allagain') group by d.device order by count(*) limit 1"
    sql="select device from device where isauto1=1 order by rand() limit 1"
    cur.execute(sql)
    for each in cur:
        (device,)=each
    #假如获取到空的结果集
    #手趣聚合渠道需要用支付宝支付，目前只有海信A1（2）这台有支付宝
    if channel_id=="shouqu":
        device="df2fca41"
    if device=='':
        if channel_id=="dalan":
            device="df22ca99"
        k=random.randint(1,100)
        if k>55:
            #device="SSHUQOC6SCZLVS8L"
            device = "df2fca41"

    #渠道177不一定是大蓝ysdk包，需要判断下
    if apk.find("ysdk_dalan")==-1 and channel=="177":
        #渠道改为君海应用宝
        channel_id="yingyongbao"
    payload = {'game': game_id, 'channel': channel_id,'apk':apk,'device':device,'user':'liyc10','d_task_id':task_id}
    r = requests.get(url1, params=payload)
    print(r.text)
    if r.text.find("插入task完成")>0:
        print("加入云测任务成功")
        sql="update yunapk set state=2 where task_id='"+task_id+"'"        
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        getpackageinfo()
    else:
        sql="update yunapk set state=0,comments='加入云测失败' where task_id='"+task_id+"'"        
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    return
class ContactsAndroidTests(unittest.TestCase):
    #driver=p.driver
    def setUp(self):
        #self.drvier=p.driverstart()
        sleep(1)
    def tearDown(self):
        sleep(1)
       

    def test_1game_update(self):

        addtask()




        
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    abc=0
    while abc>-1:
        abc=abc+1
        print("执行次数："+str(abc))
        unittest.TextTestRunner(verbosity=2).run(suite)
        sleep(10)    
