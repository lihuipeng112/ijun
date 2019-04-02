
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
from PIL import Image
import opencv
from opencv import imgcompare
import requests
import datetime
import inspect  
import ctypes
#解析ipa包需要用到
from biplist import *
import os
import zipfile
import importlib


importlib.reload(sys)

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
task_id=""
ip="192.168.1.230"
cpu=0
package=""
task_dir=""
install_flag=0
size = (540,960)
rh=0
rw=0
install_need=0
web_server="http://192.168.1.204:8080/"
device0=""
appiont_task=0
task_id1=""
if len(sys.argv)>1:
    appiont_task=1
    task_id1=sys.argv[1]
d_task_id=""


def check_ipa_info():
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    global xuqiu_id,xuqiulist_id,xuqiu_game,realgame,channel
    xuqiu_id=""
    xuqiulist_id=""
    xuqiu_game=""
    realgame=""
    channel_id1=""
    #获取xuqiuid
    sql="select xuqiu_id,id,game,game_id,channel_id1,channel from xuqiu_list where appstore_id='"+str(appstore_id)+"'"
    cur.execute(sql)
    for each in cur:        
        (xuqiuid,xuqiulist_id,xuqiu_game,realgame,channel_id1,channel)=each
        xuqiu_game=xuqiu_game.strip()
    if game_channel_id!=channel_id1:
        report("","check_ipa_info","ipa包game_channel_id"+game_channel_id+"与需求"+channel_id1+"不符")
        sql1="update xuqiu_list set state='打回',comment=contact(comment,'ipa包game_channel_id"+game_channel_id+"与需求"+channel_id1+"不符') where apk='"+apk+"'"
        try:      
            cur.execute(sql1)
            conn.commit()
        except(Exception) as e:
            print(str(e))   
        finally:
            cur.close()
            conn.close()
            return False         
    if xuqiu_game!=game:
        report("","check_ipa_info","ipa包游戏名称"+game+"与需求"+xuqiu_game+"不符")
        sql1="update xuqiu_list set state='打回',comment=contact(comment,'ipa包游戏名称"+game+"与需求"+xuqiu_game+"不符') where apk='"+apk+"'"
        try:      
            cur.execute(sql1)
            conn.commit()
        except(Exception) as e:
            print(str(e))   
        finally:
            cur.close()
            conn.close()
            return False        
    cur.close()
    conn.close()
    return True        
def get_ipa_game_channel_id(ipa_path):
    if not os.path.exists(ipa_path) or not zipfile.is_zipfile(ipa_path):
        return None
    re=""
    global game
    global version
    global package
    global game_channel_id
    game_channel_id=""
    #f1 = open('C:/vblog/game_channel_id.txt','w')
    with zipfile.ZipFile(ipa_path) as ipa:
        for file_name in ipa.namelist():
            search_str = '.app'
            index = file_name.find(search_str)
            if index != -1:
                info_plist_path = file_name[:index + len(search_str)] + '/Info.plist'

                info_dict = readPlistFromString(ipa.read(info_plist_path))            
                assert isinstance(info_dict, dict)
                game=info_dict['CFBundleDisplayName']                    
                package=info_dict['CFBundleIdentifier']
                version=info_dict['CFBundleShortVersionString']
                conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
                cur = conn.cursor()
                sql="update task set package='"+package+"',game='"+game+"',packageinfo='"+game+package+version+"',version_code='"+version+"' where id='"+str(id)+"'"
                #print(sql)
                try:
                    #print("")
                    cur.execute(sql)
                    conn.commit()         
                except(Exception) as e:
                    print(str(e))   
                finally:
                    cur.close()
                    conn.close()
                try:

                    game_channel_id=info_dict.get('junhaiChannel').get('gameChannelId')                    
                    print(re)
                except AttributeError:
                    #return None
                    print("error")
                    #re=""
                finally:
                    if re=="":
                        return None
                    else:
                        return re

def _async_raise(tid, exctype):  
    """raises the exception, performs cleanup if needed"""  
    tid = ctypes.c_long(tid)  
    if not inspect.isclass(exctype):  
        exctype = type(exctype)  
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))  
    if res == 0:  
        raise ValueError("invalid thread id")  
    elif res != 1:  
        # """if it returns a number greater than one, you're in trouble,  
        # and you should call it again with exc=NULL to revert the effect"""  
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)  
        raise SystemError("PyThreadState_SetAsyncExc failed")  
  
def stop_thread(thread):  
    _async_raise(thread.ident, SystemExit)
def download(f):
    global f1
    print("downloading with requests")
    id=""
    code=""
    t1=datetime.datetime.now()
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    #sql="select y.task_id from xuqiu_list l,yunapk y,xuqiu x,task t where y.task_id=l.d_task_id and x.id=l.xuqiu_id and x.state=1 and y.state=2 and l.state='已提测' and l.channel='腾讯ysdk' and t.d_task_id=y.task_id and t.a_state in ('new','allagain')  order by l.xuhao limit 1"
    #task和xuqiu_list中存在这个包id,xuqiu_list是xuqiu下的，需求没有关闭，需求已提测，task的状态为new或allagain，l.x_state=1，task中的包id不为空，指定某一台设备，设备处于空闲状态，该设备连接到登陆的服务器，根据优先级排序，取一行数据
    sql="select id,code from waiwangtibao where wenjian='"+f+"'"
    cur.execute(sql)
    for each in cur:        
        (id,code)=each
    cur.close()
    conn.close()
    if id=="" or code=="":
        print("数据库无此文件数据")
        return
    #url="http://192.168.1.204:8080/dinner/download.jsp?id="+id+"&code="+code
    url = 'http://192.168.1.204:8080/dinner/download.jsp?id=%s&code=%s' % (id, code)

    f1='/yuntest/apks/'+ f      
    #r = requests.get(url,timeout=150)
    r = requests.get(url)
    with open(f1, "wb") as code:
         code.write(r.content)
    t2=datetime.datetime.now()
    print("use time:"+str((t2-t1).seconds))    
    return

def download1(f):
    global f1
    t1 = datetime.datetime.now()

    f1 = '/yuntest/apks/' + f
    # r = requests.get(url,timeout=150)
    t2 = datetime.datetime.now()
    print("use time:" + str((t2 - t1).seconds))
    return

def upload(pic):
    url=web_server+"addpic1.jsp"
    data = {'task_id': str(task_id)}
    files ={'file': open(pic, 'rb')}
    response = requests.post(url, data=data, files=files)
    return
def setinfo():
    return
def adb_shot():
    global rh
    global rw
    pic=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+".png"
    pic1=task_dir + "/" + pic
    pic2=pic1.replace(".png",".jpeg")
    '''
    cmdrun("adb -s "+ device + " shell < /home/work/yuntest/shotcom.txt")
    sleep(2)
    cmdrun("adb -s "+ device + " pull /sdcard/screenshot.png "+ pic1)
    '''
    cmdrun("adb -s "+ device + " shell screencap -p | sed 's/\r$//' > "+pic1)
    print(pic1)
    if not os.path.isfile(pic1):
        report("","安装","没截到图，返回")
        return ""
    try:        
        img = Image.open(pic1)
        #rh=img.size['height']
        #rw=img.size['width']
        (rw,rh)=img.size
        #print(img.size)
        img.thumbnail(size)
        img.save(pic2, "JPEG")
        upload(pic2)
    except(Exception) as e:
        print(str(e))
        return ""
    return pic2
def adbtouch(x0,y0):
    #(x0,y0)=b
    #size=driver.get_window_size()
    #print("size1"+str(size['height']))
    #print("size1"+str(size['width']))

    #report("","游戏界面大小height:"+str(height)+",width:"+str(width),"done")

    print("竖屏游戏")
    y=int(rh*y0/1920)
    x=int(rw*x0/1080)

    cmd="adb -s "+device+" shell input tap "+str(x)+" "+str(y)
    #report("","adb touch",cmd)
    cmdrun(cmd)
def uninstall():
    global re
    #卸载
    print("uninstall apk")
    if channel_script!="":
        re=cmdrun("adb -s "+device+" uninstall "+package)
def installing():
    global install_flag
    if install_need==0:
        report("","","安装不需要同意")
        return
    device_not="df22ca99,SSHUQOC6SCZLVS8L"
    if device_not.find(device)>-1:
        return
    path="/home/work/yuntest/before_install_pic"
    if os.path.exists(path+"/"+device0):
        path=path+"/"+device0
        print(path)
        report("","install pic路径变更",path)
    fileList = []
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path + '/' + f) and (f.find(".jpeg")>0 or f.find(".jpg"))>0:
            fileList.append(path + '/' + f)
    sleep(1)
    while install_flag>0:
        install_flag=install_flag-1
        pic=adb_shot()
        for f in fileList:
            a,x,y=opencv.imgcompare(pic,f)
            #print(a)
            if a:                
                adbtouch(x,y)
                #break
 
    print("安装检查退出")            

    return
def cmdrun(command):
    if command.find("install")>-1 and command.find("uninstall")==-1:
        cmd = "ps -ef | grep 'install /' | wc -l"
        p = os.popen(cmd)        
        pid = p.readline().strip()
        k=0
        while int(pid)>5 and k<100:
            sleep(5)
            k=k+1
            p = os.popen(cmd)        
            pid = p.readline().strip()            
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    out += err
    return out
def getcpu():
    total_mem=""
    while cpuf==0:
        cpu=""
        mem=""
        if total_mem=="":
            cmd="adb -s " + device + " shell cat /proc/meminfo | grep MemTotal"
            re=cmdrun(cmd)
            if re!="":
                pac=re.split ("\n")
                pack=pac[0].replace(" ","")
                total_mem=pack.replace("MemTotal:", "")
                total_mem=total_mem.replace("kB", "")
        cmd = "adb -s " + device + " shell top -n 1 | grep " + package
        re=cmdrun(cmd)
        if re!="":
            pac=re.split ("\n")
            #print(pac[0])
            pack=pac[0].split("%")
            
            cpu=pack[0]
            print(cpu)
            cpu=cpu[-3:]
            print(cpu)
            cpu=cpu.strip()
            pack=pac[0].split("K")
            if len(pack)>1:
                mem=pack[1].replace(" ","")
        sql = "insert mcpu (task_id,cpu,total_mem,mem,time) values ('" +str(task_id)+ "','" + cpu + "','" + total_mem + "','" + mem + "',now())"
        conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
        cur = conn.cursor()
        try:
        #print("")
            cur.execute(sql)
            conn.commit()         
        except(Exception) as e:
            print(str(e))   
        finally:
            cur.close()
            conn.close()
        sleep(10)
    return
def report(tc,mo,msg):    
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    sql="insert run_log (task_id,tc,mo,msg,update_time) values ('"+str(task_id)+"','"+tc+"','"+str(mo)+"','"+str(msg)+"',now())"
    #print(sql)
    try:
        #print("")
        cur.execute(sql)
        conn.commit()         
    except(Exception) as e:
        print(str(e))   
    finally:
        cur.close()
        conn.close()
    return
def updatetask(state,msg):
    print("更新任务："+str(task_id)+",状态："+state+",备注:"+msg)
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()    
    sql="update task set a_state='"+state+"',comments='"+msg+"',run_times=run_times+1,end_time=now() where id="+str(task_id)
    try:
        #print("")
        cur.execute(sql)
        conn.commit()         
    except(Exception) as e:
        print(str(e))   
    finally:
        cur.close()
        conn.close()
    return


def fabao():
    print("发包："+str(apk))
    report("","发包","start")
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    '''
    xuqiu_id=""
    xuqiulist_id=""
    xuqiu_game=""
    realgame=""
    #获取xuqiuid
    sql="select xuqiu_id,id,game,game_id from xuqiu_list where appstore_id='"+str(appstore_id)+"'"
    cur.execute(sql)
    for each in cur:        
        (xuqiuid,xuqiulist_id,xuqiu_game,realgame)=each
        xuqiu_game=xuqiu_game.strip()
    '''
    #获取游戏包包相关参数
    #game=""
    
    game_id=""
    
    channel_id="appstore"
    
    sql="select f.game_id from task t,fabao f where t.id='"+str(task_id)+"' and t.game=f.game order by f.id desc limit 1"
    cur.execute(sql)
    for each in cur:        
        (game_id,)=each

    #获取渠道参数
    #channel=""
    channel_id1="2050"
    game_channel_id=""
    y_game=""



          
    
    #sql="INSERT fabao (xuqiu_id,realgame,game,game_id,package,channel,channel_id,channel_id1,game_channel_id,apk,date,type,user) values ('" & xuqiuid & "','" & Text11.text & "','" & Text6.text & "','" & text4.text & "','" & packagename & "','" & Text7.text & "','" & Text5.text & "','" & Text10.text & "','" & Text13.text & "','" & apk1 & "',date_format(SYSDATE(),'%Y-%m-%d'),'正式','云测') on duplicate key update xuqiu_id='" & xuqiuid & "',realgame='" & Text11.text & "',game='" & Text6.text & "',channel='" & Text7.text & "',channel_id='" & Text5.text & "',channel_id1='" & Text10.text & "',package='" & packagename & "',xuqiu_id='" & xuqiuid & "',type='" & Combo4.text & "',game_id='" & text4.text & "',game_channel_id='" & Text13.text & "',state=1"
    sql="INSERT fabao (xuqiu_id,realgame,game,game_id,package,channel,channel_id,channel_id1,game_channel_id,apk,date,type,user) values ('"+str(xuqiu_id)+"','"+realgame+"','"+game+"','"+str(game_id)+"','"+package+"','"+channel+"','"+channel_id+"','"+str(channel_id1)+"','"+str(game_channel_id)+"','"+apk+"',date_format(SYSDATE(),'%Y-%m-%d'),'正式','云测') on duplicate key update xuqiu_id='"+str(xuqiu_id)+"',realgame='"+realgame+"',game='"+game+"',channel='"+channel+"',channel_id='"+channel_id+"',channel_id1='"+str(channel_id1)+"',package='"+package+"',xuqiu_id='"+str(xuqiu_id)+"',type='正式',game_id='"+game_id+"',game_channel_id='"+str(game_channel_id)+"',state=1"
    sql1="update xuqiu_list set state='已出包',chubao_time=now() where id="+str(xuqiulist_id)
    try:
        #print("")
        cur.execute(sql)
        conn.commit()         
        cur.execute(sql1)
        conn.commit()
    except(Exception) as e:
        print(str(e))   
    finally:
        cur.close()
        conn.close()
        report("","发包","完成")
    return    
def tcfenxi():
    print("tcfenxi")
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    tcsum=0
    tcsu=0
    tcfail=0
    t_state=""

    sql="select count(*) from task_testcase where task_id='"+str(task_id)+"' and state='成功'"
    #print(sql)
    cur.execute(sql)
    for each in cur:        
        (tcsu,)=each

    #tcsum改为读取run log里的案例数
    sql="select count(*) from run_log where task_id="+str(task_id)+" and tc<>'' group by tc"
    #print(sql)
    cur.execute(sql)
    rows=cur.fetchall()    
    for each in rows:        
        tcsum=tcsum+1  
    
    sql="select count(*) from task_testcase where task_id='"+str(task_id)+"' and state='失败'"
    #print(sql)
    cur.execute(sql)
    for each in cur:        
        (tcfail,)=each
    #print("tcsum" + str(tcsum))
    #print("tcfail"+str(tcfail))
    sql1=""
    if tcsum>3 and tcfail==0 and tcsum==tcsu:
        sql="update task set a_state='成功',end_time=now(),run_times=run_times+1,update_time=now() where id='"+str(task_id)+"'"
        #sql1="update yunapk set a_state='成功' where task_id='"+d_task_id+"'"
        
    else:
        sql="update task set a_state='失败',end_time=now(),run_times=run_times+1,update_time=now() where id='"+str(task_id)+"'"
        t_state="失败"
        #dahui()
    cur.execute(sql)
    conn.commit()
    if sql1!="":
        cur.execute(sql1)
        conn.commit()        
      
    cur.close()
    conn.close()
    if tcsum>3 and tcfail==0 and tcsum==tcsu:
        fabao()
    return
def gettask():
    print("gettask开始")
    global task_id
    global apk_dir
    global apk
    global device
    global channel_id
    global channel_script
    global game_id
    global package
    global task_dir
    global install_need
    global device0
    global appiont_task
    global d_task_id
    global appstore_id
    global apk_url
    install_need=0
    apk_url=""
    task_id=""
    apk_dir=""
    apk=""
    device=""
    channel_id=""
    channel_script=""
    game_id=""
    mip=""
    d_task_id=""
    appstore_id=""
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    #sql="select y.task_id from xuqiu_list l,yunapk y,xuqiu x,task t where y.task_id=l.d_task_id and x.id=l.xuqiu_id and x.state=1 and y.state=2 and l.state='已提测' and l.channel='腾讯ysdk' and t.d_task_id=y.task_id and t.a_state in ('new','allagain')  order by l.xuhao limit 1"
    #task和xuqiu_list中存在这个包id,xuqiu_list是xuqiu下的，需求没有关闭，需求已提测，task的状态为new或allagain，l.x_state=1，task中的包id不为空，指定某一台设备，设备处于空闲状态，该设备连接到登陆的服务器，根据优先级排序，取一行数据
    sql="select l.appstore_id from xuqiu_list l,xuqiu x,task t,device d where t.appstore_id=l.appstore_id and x.id=l.xuqiu_id and x.state=1 and l.state='已提测' and t.a_state in ('ready','again') and l.x_state=1 and l.appstore_id<>'' and d.device=t.device and d.is_lock=0 order by l.xuhao limit 1"
    cur.execute(sql)
    for each in cur:        
        (appstore_id,)=each
    if appstore_id=="":
        print("appstore_id 为空，下一轮")
        cur.close()
        conn.close()
        sleep(10)
        #sleep(random.randint(1,30))
        return    
    sleep(random.randint(1,10))
    #sql="select t.id,t.dir,t.apk,t.device,t.channel_id,t.channel_script,t.game_id,d.ip from task t,device d where t.a_state in ('new','allagain') and t.device=d.device and d.machine=(select user()) and d.is_lock=0 order by t.a_state desc,t.establish_time limit 1"
    #sql="select t.id,t.dir,t.apk,t.device,t.channel_id,t.channel_script,t.game_id from task t,device d where t.a_state in ('new','allagain') and t.device=d.device and d.machine=(select user()) and d.is_lock=0 order by t.a_state desc,t.establish_time limit 1"
    #sql="select t.id,t.dir,t.apk,t.device,t.channel_id,t.channel_script from task t,device d where t.a_state in ('new','allagain') order by t.establish_time limit 1"
    #task的状态为new或allagain，指定的设备，连接到登陆的服务器，设备处于空闲状态，根据上面筛选出来的包id，取一条数据
    sql="select t.id,t.dir,t.apk,t.device,t.channel_id,t.channel_script,t.game_id,d.ip from task t,device d where t.a_state in ('ready','again') and t.device=d.device and d.is_lock=0 and appstore_id='"+appstore_id+"' limit 1"
    if appiont_task==1:
        #appiont_task=0
        # task的状态为new或allagain，指定的设备，连接到登陆的服务器，设备处于空闲状态，指定的task_id
        sql="select t.id,t.dir,t.apk,t.device,t.channel_id,t.channel_script,t.game_id,d.ip from task t,device d where t.a_state in ('ready','again') and t.device=d.device and d.is_lock=0 and t.id='"+task_id1+"'"
    cur.execute(sql)
    for each in cur:
        (task_id,apk_dir,apk,device,channel_id,channel_script,game_id,mip)=each
    #cur.close()
    #conn.close()
    device0=device

    print("task_id " + str(task_id))
    print("apk_dir " + str(apk_dir))
    print("apk " + str(apk))
    print("device " + str(device))
    print("channel_id " + str(channel_id))
    print("channel_script " + str(channel_script))
    if task_id=="":
        print("task_id 为空，等待10s")        
        cur.close()
        conn.close()
        sleep(10)
        return
    else:
        #锁任务
        sql="update task set a_state='doing',start_time=now(),update_time=now() where id='"+str(task_id)+"' and a_state in ('ready','again')"
        num=cur.execute(sql)
        conn.commit()
        if str(num)=="0":
            print("重复获取任务，等待下一次")        
            cur.close()
            conn.close()
            sleep(1)
            return            
        #锁设备        
        sql="update device set is_lock=1,update_time=now() where device='"+device+"' and is_lock=0"
        num=cur.execute(sql)
        conn.commit()
        if str(num)=="0":
            print("设备被锁，等待下一次")
            #更新任务状态回去
            sql="update task set a_state='again',update_time=now() where id='"+str(task_id)+"' and a_state='doing'"
            num=cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            sleep(1)
            return 
    if channel_script=="" :
        print("渠道脚本为空")
        cur.close()
        conn.close()
        updatetask("失败","渠道脚本为空")        
        return

    
    if apk.find(".ipa")==-1:
        cur.close()
        conn.close()
        updatetask("失败","被测包不是ipa安装文件")        
        return
        
    if apk.find(".ipa")>-1:
        #锁任务、设备、appium server
        '''
        sql="update task set a_state='doing',start_time=now(),update_time=now() where id='"+str(task_id)+"'"
        cur.execute(sql)
        conn.commit()
        '''
        dlock=0
        install_need=0

        sql="update server set run_times=run_times+1,state=0,device='"+device+"' where state=1 and machine=(select user()) order by rand() limit 1"
        cur.execute(sql)
        conn.commit()
        #cur.close()
        #conn.close()
        
        #检查task目录
        file_dir="/yuntest/task/"+str(task_id)
        # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        #apk复制
        napk=task_dir +"/"+apk
        
        if not os.path.isfile(napk) :
            #getpackageinfo
            #re=cmdrun("cp /home/work/yuntest/server/upload/"+apk+" /home/work/yuntest/apks/")
            #print(re)
            #从云测下载包

            download(apk)
            sleep(3)
        #get ipa包的信息

        f1 = '/Volumes/ntfs3/ios_python/apk.ipa'
        get_ipa_game_channel_id(f1)
        #检测ipa包跟需求
        if not check_ipa_info():
            cur.close()
            conn.close()
            return
        #脚本复制
        #pycopy()
        channel_script="/Volumes/ntfs3/ios_python/"+channel_script
        #脚本执行
        
        yunce()
    return

def yunce():
    global cpuf
    global install_flag
    #install()
    #os.system("adb -s "+device+" install "+apk_dir+"/"+apk)
  
    sleep(5)
    print("调起获取手机性能数据函数")


    print("调起游戏脚本")
    report("","","调起游戏脚本"+channel_script)

    os.system("python "+channel_script +" " +str(task_id))
    sleep(5)
    #停掉手机获取性能过程
    report("","","tcfenxi")
    tcfenxi()
    return

def unlock():
    #t = threading.Thread(target=uninstall,name=device)
    #t.setDaemon(True)
    #t.start()
    #解锁device、server url
    print("unlock device、server url")
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
    cur = conn.cursor()
    
    sql="update device set is_lock=0 where device='"+device+"'"

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
        unlock()
       

    def test_1game_update(self):

        gettask()




        
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    abc=0
    while 1==1:
        
        abc=abc+1
        print("执行次数："+str(abc))
        conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password',db='autotest',charset='utf8')
        cur = conn.cursor()
        stop=0
        sql="select stop from machine where machine=(select user())"
        cur.execute(sql)
        for each in cur:        
            (stop,)=each
        cur.close()
        conn.close()
        print(stop)
        if stop==1:
            print("task 退出")
            break          

        unittest.TextTestRunner(verbosity=2).run(suite)
        sleep(10)
        '''
        d_task_id="10963"
        task_id="15443"
        apk="qyj_agent_102098_yyb_ysdk_bingniao_10029_1.24.0_20170615_10963.apk"
        fabao()
        '''
        t = threading.Thread(target=uninstall,name=device)
        if t.isAlive(): 
            stop_thread(t) 
        if appiont_task==1:
            break
        
    #update()
    


