#/usr/local/Cellar/python/3.6.5/bin/python3
# -*- coding: utf-8 -*-
import wda
from time import sleep
import shell_set_app
import pymysql
import sys,os
import time
from PIL import Image
import shlex
from subprocess import Popen,PIPE
import subprocess
import requests
import json
import datetime

ip = '192.168.1.230'
file = sys.argv[0]
testcase = ''
auto_shot = 1
package=''
order_sn_ysdk=''
order_sn_1=''
order_sn=''
shiyuan_price=''
shiyuan_name=''
game_xuhao=0
channel_xuhao=0
version_code=""
game_channel_id=""
channel_id1 =''
device_id=""
web_server="http://192.168.1.204:8080/"
c = wda.Client()
account = ''
password = ''

size = (1334, 750)
intgametype = 1



def clear_appitunes():
    '''
    清除APP账号
    '''
    global c
    c = wda.Client()
    report('', 'setting', '配置账号信息')
    sleep(3)
    with c.session() as s:
        m1 = s(name='设置').exists
        if m1:
            print('打开设置')
            s(name='设置').get(timeout=10).tap()
            sleep(3)
            m2 = s(name='iTunes Store 与 App Store').exists
            new_id_e = s(name='创建新 Apple ID').exists
            print('itunes', m2)
            if m2 and new_id_e:
                #从上次注销完账号之后回到设置界面
                s(name='设置').get(timeout=10).tap()
            if m2:
                itunes = s(name='iTunes Store 与 App Store').get(timeout=10)
                itunes.scroll()
                itunes.tap()
                #判断是否有iTunes账号,true代表没有登录账号
                m3 = s(name='登录').exists
                print('判断是否有登录账号，没有登录账号输出true:',m3)
                if m3:
                    #没有登录账号
                    s().wait(2.0)
                    print('没有登录账号,准备安装APP')
                else:
                    print('有登录账号，准备注销用户ID')
                    sleep(3)
                    s(predicate='name LIKE "Apple ID*"').tap()
                    s().wait(2)
                    sleep(3)
                    s(name='注销').get(timeout=10).tap()
                    print('注销完成，准备安装APP')
                s(name='设置').get(timeout=10).tap()

    c.home()

def convert1(data):
    '''

    :param data: 传入一个字典
    :return: 将非字典中的非字符串，转化为字符串
    '''
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert1, data.items()))
    if isinstance(data, tuple):  return map(convert1, data)
    return data

def setinfo(str1):
    global game_id
    global device
    global package
    global activity
    global gameexe
    global apk
    global channel_id
    global channel_id1
    global device_name
    global mip
    global game1
    global d_task_id
    global device_id
    global yueka_price
    global yueka_name
    global shiyuan_price
    global shiyuan_name
    global task_id
    global ud_id
    global driver
    global w_id
    global w_code
    global w_wenjian
    global w_comment
    global sql
    global w_apk
    global company
    global account
    global password
    task_id = str1
    print('setinfo:',task_id)

    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='utf8')
    cur = conn.cursor()
    #从task表中读取任务信息
    sql = "select t.id,t.device,t.package,t.activity,t.game_exe,t.apk,t.yueka_price,t.yueka_name,t.shiyuan_price,t.shiyuan_name,t.channel_id,t.game_id,d.name,d.ip,t.game,d.udid from task t,device d where t.id = '%s' and t.device = d.device" % task_id
    cur.execute(sql)
    for each in cur:
        #each = convert(each)
        device = each[1]
        device0=device
        package = each[2]
        activity = each[3]
        gameexe = each[4]
        apk = each[5]
        apk = apk.strip()
        w_apk = apk
        yueka_price = each[6]
        yueka_name = each[7]
        shiyuan_price = each[8]
        shiyuan_name = each[9]
        channel_id = each[10]
        game_id = each[11]
        device_name = each[12]
        mip = each[13]
        game1=each[14]
        ud_id = each[15]
        print(device,ud_id,apk)
    report('','',package)
    cur.close()
    conn.close()
    # 在wuqiu_list中找到channel_id，即game_channerl_id
    # apk = 'ymsj_songshu16_appstore_dev_v1.0.0_110_20180208_1.ipa'
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    cur = conn.cursor()
    sql = "select channel_id1 from xuqiu_list where apk = '" + w_apk + "'"
    print(sql)
    cur.execute(sql)
    for each in cur:
        channel_id1 = each[0]

    #conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    #cur = conn.cursor()
    sql = "select company,account,password from appstore where game_id = '" + channel_id1 + "'"
    print(sql)
    cur.execute(sql)
    for each in cur:
        company = each[0]
        account = each[1]
        password = each[2]

    #模拟task中有这个apk信息
    #获取外网发包信息,下载安装文件到本地
    sql = "select id,code,wenjian,comment from waiwangtibao where wenjian = '%s'" % apk
    cur.execute(sql)
    #print(sql)
    for each in cur:
        t1 = datetime.datetime.now()

        print('准备下载文件中')
        report('app','下载成功','')
        w_id = int(each[0])
        w_code = int(each[1])
        w_wenjian = each[2]
        w_comment = each[3]
        print(w_wenjian)
        '''
        apk = 'http://192.168.1.204:8080/dinner/download.jsp?id=%s&code=%s' % (w_id,w_code)

        try:
            r = requests.get(apk, stream=True)
            if r.status_code == 200:
                print('请求成功，正在下载')
            with open('apk.ipa', "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
        except(Exception) as e:
            print(str(e))
            cur.close()
            conn.close()
            return ""
        cur.close()
        conn.close()
        t2 = datetime.datetime.now()
        print('下载文件完成,下载总时间：'+ str((t2 - t1).seconds))
        report('','下载文件成功','end')
        '''
        #apk = 'apk.ipa'
        apk = '/Volumes/E/yuntest/apks/' + apk
        print(apk)

def report(tc,mo,msg):
    global testcase
    global sql
    #testcase = 'lhp'
    #task_id = '10062'
    if tc!="":
        testcase = tc

    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    cur = conn.cursor()
    if msg=='fail':
        sql = "insert run_log(task_id,tc,mo,msg,shot,update_time) values('"+task_id+"','"+str(testcase)+"','"+str(mo)+"','"+str(msg)+"','"+shot()+"',now())"
    else:
        sql = "insert run_log(task_id,tc,mo,msg,update_time) values('"+task_id+"','"+str(testcase)+"','"+str(mo)+"','"+str(msg)+"',now())"

    try:
        cur.execute(sql)
        conn.commit()
    except(Exception) as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()
        sleep(1)
    return

def report1(tc,mo,msg):
    global testcase
    global sql
    #testcase = 'lhp'
    if tc!="":
        testcase = tc

    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    cur = conn.cursor()
    if msg=='fail':
        sql = "insert run_log(task_id,tc,mo,msg,shot,update_time) values('"+task_id+"','"+str(testcase)+"','"+str(mo)+"','"+str(msg)+"','"+shot()+"',now())"

    try:
        cur.execute(sql)
        conn.commit()
    except(Exception) as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()
    return


def report2(tc, mo, msg, pic):
    global testcase
    # mo=unicode(mo).encode("utf-8")
    if tc != "":
        testcase = tc
    print(testcase + "," + mo + "," + msg)
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='utf8')
    cur = conn.cursor()
    # if msg=="fail":

    sql = "insert run_log (task_id,tc,mo,msg,shot,update_time) values('" + task_id + "','" + str(
        testcase) + "','" + str(mo) + "','" + str(msg) + "','" + pic + "',now())"
    # else:
    # sql="insert run_log (task_id,tc,mo,msg,update_time) values('"+task_id+"','"+str(testcase)+"','"+str(mo)+"','"+str(msg)+"',now())"
    # print("report2,"+sql)
    try:
        cur.execute(sql)
        conn.commit()
    except(Exception) as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()
    return
def upload(pic):
    #import requests
    url=web_server+"addpic1.jsp"
    data = {'task_id': str(task_id)}
    files ={'file': open(pic, 'rb')}
    response = requests.post(url, data=data, files=files)
    print(response)
    return

def shot1():


    #task_id = '10062'
    #testcase = '11'
    #截图要保存的名称及位置
    pic = testcase + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) +'.png'

    #截取当前截图
    c.screenshot('shot.png')
    img1 = Image.open('shot.png')
    #创建一个新目录
    imagename = '/Users/lichun/Documents/lihui/' + str(task_id) +'/' + pic
    #放到云测上时换用此路径
    #imagename = '/home/work/yuntest/task/' + str(task_id) + '/' + pic
    file_dir = os.path.split(imagename)[0]

    # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)

    # 然后再判断文件是否存在，如果不存在，则创建
    if not os.path.exists(imagename):
        os.system(r'touch %s' % imagename)

    infile = imagename
    outfile = infile.replace(".png", ".jpeg")

    #将图片保存到指定游戏的位置
    # RGB -> JPG
    im = Image.open('shot.png')
    rgb_im = im.convert('RGB')
    rgb_im.save(outfile)
    #img1.save(imagename)
    if not os.path.isfile(imagename):
        report('','shot'+imagename,'没有截到图，返回')
        return ''


    print(infile,outfile)
    outfile1 = "/home/work/yuntest/server/task/" + str(task_id) + "/shot/"

    try:
        upload(outfile)
    except(Exception) as e:
        print(str(e))
        return ""

    return outfile

def shot():


    #task_id = '10062'
    #testcase = '11'
    #截图要保存的名称及位置
    pic = testcase + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) +'.png'

    #截取当前截图
    c.screenshot('shot.png')
    img1 = Image.open('shot.png')
    #创建一个新目录
    imagename = '/Volumes/yuntest/python/task/' + str(task_id) +'/shot/' + pic
    #放到云测上时换用此路径
    #imagename = '/home/work/yuntest/task/' + str(task_id) + '/' + pic
    file_dir = os.path.split(imagename)[0]

    # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)

    # 然后再判断文件是否存在，如果不存在，则创建
    if not os.path.exists(imagename):
        os.system(r'touch %s' % imagename)

    infile = imagename
    outfile = infile.replace(".png", ".jpeg")

    #将图片保存到指定游戏的位置
    # RGB -> JPG
    im = Image.open('shot.png')
    rgb_im = im.convert('RGB')
    rgb_im.save(outfile)
    #img1.save(imagename)
    if not os.path.isfile(imagename):
        report('','shot'+imagename,'没有截到图，返回')
        return ''



    return outfile
def sessionstart():
    global s
    global c
    #eport('','准备启动游戏','start')
    c = wda.Client()
    s = c.session(package)
    #report('','启动游戏','done')
    return s
def sessionquit():
    global s
    c.session(package).close()
    return


def begin(task_id):
    try:
        global c
        c = wda.Client()
        c.home()
    except(Exception) as e:
        print(str(e))


    clear_appitunes()

    shell_set_app.set_app(package, ud_id, apk)

    apps = shell_set_app.get_all_app()
    if package in apps:
        #打开app
        s = c.session(package)
        report('app','打开app','tcend')
        sleep(5)
        return c,s
    else:
        report('','安装失败','fail')

def gamekeep():
    global thflag
    global c
    c = wda.Client()
    i = 0
    while thflag!='done':
        print('game---',i)
        if i % 30==0 and auto_shot==1:
            report1('','游戏脚本执行中','截图')
        i = i + 1
        sleep(1)
        try:
            c = wda.Client()
        except(Exception) as e:
            print('gamekeep异常'+str(e))
            report1('','gamedeep','异常')
            continue
    return

def game(tc):
    '''
    global tc1
    global thflag
    thflag = ''
    tc1 = tc
    report(testcase,'游戏testcast启动',tc)
    t = threading.Thread(target=gamekeep)
    t.setDaemon(True)
    t.start()
    '''
    global tc1
    global thflag
    thflag = ''
    tc1 = tc
    report(testcase,'游戏testcase启动',tc)
    try:
        exec('from '+game_id+' import '+tc)
        runtc = eval(tc)
        re=runtc()
    except(Exception) as e:
        #thflag='done'
        print("run"+game_id+'tc:'+str(tc)+'异常：'+str(e))
        thflag = 'done'
        return
    #thflag = 'done'
    sleep(3)
    return re


def cmdrun(cmd):
    p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    out,err = p.communicate()
    out +=err
    return out

def touch(session, x, y):
    if session.orientation == 'LANDSCAPE':
        window_size = session.window_size()
        fix_x = y
        fix_y = window_size.height - x
    else:
        fix_x = x
        fix_y = y
    session.tap(fix_x, fix_y)

def tcfenxi():

    report1('','testcase分析','start')
    sql = ''
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    cur = conn.cursor()
    sql = "select * from run_log where task_id = '"+task_id+"' and tc='"+testcase+"' and msg='fail'"
    cur.execute(sql)
    if int(cur.rowcount)>0:
        sql = "insert task_testcase(task_id,testcase,state,lastupdate_time) values('"+task_id+"','"+str(testcase)+"','失败',now()) on duplicate key update state = '失败',lastupdate_time=now()"
    else:
        sql = "select * from run_log where task_id='"+task_id+"' and tc='"+testcase+"' and msg='tcend'"
        cur.execute(sql)
        if int(cur.rowcount)>0:
            sql = "insert task_testcase (task_id,testcase,state,lastupdate_time) values('"+task_id+"','"+str(testcase)+"','成功',now()) on duplicate key update state = '成功',lastupdate_time=now()"
        else:
            sql = "insert task_testcase (task_id,testcase,state,lastupdate_time) values('" + task_id + "','" + str(testcase) + "','失败',now()) on duplicate key update state = '失败',lastupdate_time=now()"

    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

    if str(testcase)=='yueka':
        global order_sn
        global order_sn_ysdk
        if channel_id.find('ysdk')>-1:
            order_sn_ysdk = order_sn
        order_sn =''
    return

def updatetask():
    report('','更新任务状态','start')
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    cur = conn.cursor()
    cur.execute("select * from task_testcase where task_id = '"+task_id+"' and state='失败'")
    if int(cur.rowcount)>0:
        sql = "update task set a_state='失败',end_time=now() where id ='"+task_id+"'"
    else:
        sql = "update task set a_state='成功',end_time=now() where id ='" + task_id + "'"

    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    report('','更新任务状态','end')
    return

def urlget(url1):
    try:
        r = requests.get(url1,timeout=60)
        return r.text
    except(Exception) as e:
        print(str(e))
        return str(e)

def getorderstate(sn):
    re_url = "http://122.226.199.75/agent/api/agentOrderInfo?order_sn=" + str(sn)
    re_url = "http://agent.ijunhai.com/api/agentOrderInfo?order_sn=" + str(sn)
    re = urlget(re_url)
    try:
        rejson = json.loads(re, encoding='utf-8')
    except(Exception) as e:
        print(str(e))
    if str(rejson['ret']) == '1':
        print("请求成功，结果是：" + re)
        report("", "请求成功，结果是：", str(re))
        if str(rejson['content']['status']) == "4":
            return True
        else:
            report('', '请求订单结果', str(re))
            return False
    else:
        report('', '请求订单结果', str(re))
        return False

def checkweb():
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    cur = conn.cursor()
    sql = "select * from task_testcase where task_id = '" + task_id + "' and state='失败'"
    try:
        cur.execute(sql)
        if int(cur.rowcount) > 0:
            print('有失败，不执行')
            return ''
    except(Exception) as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()
    url = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=2050&device_id=E062161B-8DD5-4C51-8C61-720CBC29724C&time=2018-03-07&game_channel_id=104044'
    #url1 = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=10447&device_id=ffffffff-98a0-a82a-adcc-64ce0033c587&time=2018-03-07&game_channel_id=104308'
    nowtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    check_url = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=2050&device_id=E062161B-8DD5-4C51-8C61-720CBC29724C&time=%s&game_channel_id=%s' % (nowtime,channel_id1)
    print(check_url)
    if getorder_sn():
        print('之前存在订单')
        report('dd_data','之前存在订单','二次判断')
        i = 0
        while i < 10:
            sleep(i * 10)
            i += 1
            try:
                re = requests.get(check_url)
                print(i, re.status_code)
                hjson = json.loads(re.text)
                content = hjson['content']
                order = content['order']
                order_content = order['content']

                # status=4 ：通知研发成功，pay_status=1：渠道通知订单支付
                status = order_content['status']
                pay_status = order_content['pay_status']
                order_sn1 = order_content['order_sn']
                goods_name = order_content['goods_name']
                money = order_content['money']
                six_money = int(float(money))
                if order_sn == order_sn1:
                    report('', '查询为之前的订单', '重新查询'+str(i))
                    print('查询为之前的订单')
                    continue
                if status == '4' and pay_status == '1' and goods_name == '元宝' and six_money == 6:
                    print(order_content['order_sn'], order_content['game_role_name'])
                    report('dd_data', '付款角色', order_content['game_role_name'])
                    report('dd_data','付款订单',order_content['order_sn'])
                    report('dd_data', '付款类型', order_content['goods_name'])
                    report('dd_data', '付款额', order_content['money'])
                    report('dd_data', 'pay', 'tcend')
                    break
                if status == '3':
                    # 通知CP失败
                    report('pay', '付款角色', order_content['game_role_name'])
                    report('dd_data', 'pay', 'fail')
                    break


                print(order_content)
            except(Exception) as e:
                print(str(e))
    else:
        print('之前不存在订单')
        i = 0
        while i < 10:
            sleep(i*10)
            try:
                re = requests.get(check_url)
                print(i,re.status_code)
                print(re.text)

                hjson = json.loads(re.text)
                content = hjson['content']
                order = content['order']
                order_content = order['content']
                if order_content == None:
                    print(order['msg'])
                    print('没有订单')
                    report('dd_data','查询独代信息',str(i))

                else:
                    print(order_content['status'],order_content['pay_status'])
                    #status=4 ：通知研发成功，pay_status=1：渠道通知订单支付
                    status = order_content['status']
                    pay_status = order_content['pay_status']
                    goods_name = order_content['goods_name']
                    money = order_content['money']
                    six_money = int(float(money))
                    if status == '4' and pay_status == '1' and goods_name == '元宝' and six_money == 6:
                        report('dd_data', '付款角色', order_content['game_role_name'])
                        report('dd_data', '付款订单', order_content['order_sn'])
                        report('dd_data', '付款类型', order_content['goods_name'])
                        report('dd_data', '付款额', order_content['money'])
                        report('dd_data', 'pay', 'tcend')
                        break
                    if status == '3':
                        #通知CP失败
                        report('pay', '付款角色', order_content['game_role_name'])
                        report('dd_data', 'pay', 'fail')
                        break
                    break
                i += 1
                print(order_content)
            except(Exception) as e:
                print(str(e))

    print(order_content)
    if order_content == None:
        print(order['msg'])
        print('没有订单')
        report('dd_data','pay','fail')

def checkweb1():
    global order_sn
    url = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=2050&device_id=E062161B-8DD5-4C51-8C61-720CBC29724C&time=2018-03-07&game_channel_id=104044'
    #url1 = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=10447&device_id=ffffffff-98a0-a82a-adcc-64ce0033c587&time=2018-03-07&game_channel_id=104308'
    nowtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    check_url = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=2050&device_id=E062161B-8DD5-4C51-8C61-720CBC29724C&time=%s&game_channel_id=%s' % (nowtime,channel_id1)
    try:
        re = requests.get(check_url)
        print(re.text)

        hjson = json.loads(re.text)
        content = hjson['content']
        order = content['order']
        order_content = order['content']
        if order_content == None:
            print(order['msg'])
            print('当天没有出包')
            order_sn = ''
        else:
            print(order_content['status'],order_content['pay_status'])
            #status=4 ：通知研发成功，pay_status=1：渠道通知订单支付
            status = order_content['status']
            pay_status = order_content['pay_status']
            if status == '4' and pay_status == '1':
                print(order_content['order_sn'],order_content['game_role_name'])
                order_sn = order_content['order_sn']
                report('','当天二次出包','出包订单'+ order_sn)

        print(order_content)

    except(Exception) as e:
        print(str(e))


def checkweb2():
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    cur = conn.cursor()
    sql = "select * from run_log where task_id = '" + task_id + "' and tc='pay' and msg='fail'"
    try:
        cur.execute(sql)
        if int(cur.rowcount) > 0:
            print('有失败，不执行')
            return ''
    except(Exception) as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()
    url = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=2050&device_id=E062161B-8DD5-4C51-8C61-720CBC29724C&time=2018-03-07&game_channel_id=104044'
    #url1 = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=10447&device_id=ffffffff-98a0-a82a-adcc-64ce0033c587&time=2018-03-07&game_channel_id=104308'
    nowtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    check_url = 'http://game.data.ijunhai.com/Mirana/Api/autoTest?game_id=146&channel_id=2050&device_id=E062161B-8DD5-4C51-8C61-720CBC29724C&time=%s&game_channel_id=%s' % (nowtime,channel_id1)
    print(check_url)

    i = 0
    while i < 15:
        sleep(i*9)
        try:
            re = requests.get(check_url)
            print(i,re.status_code)
            print(re.text)

            hjson = json.loads(re.text)
            content = hjson['content']
            order = content['order']
            order_content = order['content']
            if order_content == None:
                print(order['msg'])
                print('没有订单')
                report('dd_data','查询独代信息',str(i))

            else:
                print(order_content['status'],order_content['pay_status'])
                #status=4 ：通知研发成功，pay_status=1：渠道通知订单支付
                status = order_content['status']
                pay_status = order_content['pay_status']
                if status == '4' and pay_status == '1':
                    print(order_content['order_sn'],order_content['game_role_name'])
                    report('dd_data','付款角色',order_content['game_role_name'])
                    report('dd_data', 'pay', 'tcend')
                    break
                if status == '3':
                    #通知CP失败
                    report('pay', '付款角色', order_content['game_role_name'])
                    report('dd_data', 'pay', 'fail')
                    break
                break
            i += 1
            print(order_content)
        except(Exception) as e:
            print(str(e))

    print(order_content)
    if order_content == None:
        print(order['msg'])
        print('没有订单')
        report('dd_data','pay','fail')



def getorder_sn():
    report('', 'order_sn:', str(order_sn))
    if order_sn == "":
        return False
    else:
        return True


def checkpay(ph1):
    ##        while re="" and k<10:
    ##            k=k+1
    ##            re = p1.readline().strip()    
    ##            if re!="" and re.find("order_sn:")>-1:
    ##                order_sn=re
    ##            else:
    ##                report("","找不到order_sn","fail")
    ##                return
    '''
    if order_sn == "" and order_sn_1 == "":
        if channel_id.find("ysdk") > -1 and order_sn_ysdk != "":
            report("", "ysdk,订单号不为空", "执行检查")
        else:
            report("", "订单号为空", "fail")
            return
    '''
    global driver
    driver = ""
    order_re1 = False
    k = 0
    order_re = False
    order_re2 = False
    while k < 7 and not order_re and not order_re1 and not order_re2:
        k = k + 1
        sleep(10 * k)
        order_re = getorderstate(order_sn)
        if order_sn_1 != "":
            order_re2 = getorderstate(order_sn_1)
        if order_sn_ysdk != "":
            order_re1 = getorderstate(order_sn_ysdk)
    if not order_re and not order_re1 and not order_re2:
        report("", "订单:" + str(order_sn) + "状态不是请求cp发货成功", "fail")
        if order_sn_1 != "":
            report("", "订单:" + str(order_sn_1) + "状态不是请求cp发货成功", "fail")
        if order_sn_ysdk != "":
            report("", "订单:" + str(order_sn_ysdk) + "状态不是请求cp发货成功", "fail")
    else:
        if order_re:
            report("", "order_re返回订单状态", "订单:" + str(order_sn) + "状态为通知cp成功")
        if order_re1:
            report("", "order_re1返回订单状态", "订单:" + str(order_sn_1) + "状态为通知cp成功")
        if order_re2:
            report("", "order_re2返回订单状态", "订单:" + str(order_sn_ysdk) + "状态为通知cp成功")
    return


def checktask():
    report('', "检查任务状态", "start")
    ck_re = False
    sql = ""
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='utf8')
    cur = conn.cursor()
    sql = "select * from run_log where task_id='" + task_id + "' and msg='fail'"
    cur.execute(sql)
    if int(cur.rowcount) == 0:
        ck_re = True
    cur.close()
    conn.close()
    report("", "检查任务状态" + str(ck_re), "end")
    return ck_re

def ckshiyuan(price,name):
    re =1
    if price.find(shiyuan_price)>-1:
        report('','十元价格检查','与预期'+shiyuan_price+'一致，成功')
    else:
        report('', '十元价格检查', '与预期' + shiyuan_price + '不一致')
        report('','十元价格检查','fail')
        re = 0
    if name!='':
        re = 1
        if price.find(shiyuan_price) > -1:
            report('', '十元价格检查', '与预期' + shiyuan_price + '一致，成功')
        else:
            report('', '十元价格检查', '与预期' + shiyuan_price + '不一致')
            report('', '十元价格检查', 'fail')
            re = 0
    return re

def checkpay(ph1):

##        while re="" and k<10:
##            k=k+1
##            re = p1.readline().strip()
##            if re!="" and re.find("order_sn:")>-1:
##                order_sn=re
##            else:
##                report("","找不到order_sn","fail")
##                return
    '''
    if order_sn=="" and order_sn_1=="":
        if channel_id.find("ysdk") > -1 and order_sn_ysdk!="":
            report("", "ysdk,订单号不为空", "执行检查")
        else:
            report("","订单号为空","fail")
            return
    '''
    global driver
    driver=""
    order_re1=False
    k=0
    order_re=False
    order_re2=False
    while k<7 and not order_re and not order_re1 and not order_re2:
        k=k+1
        sleep(10*k)
        order_re=getorderstate(order_sn)
        if order_sn_1!="":
            order_re2 = getorderstate(order_sn_1)
        if order_sn_ysdk!="":
            order_re1 = getorderstate(order_sn_ysdk)
    if not order_re and not order_re1 and not order_re2:
        report("","订单:"+str(order_sn)+"状态不是请求cp发货成功","fail")
        if order_sn_1 != "":
            report("", "订单:" + str(order_sn_1) + "状态不是请求cp发货成功", "fail")
        if order_sn_ysdk != "":
            report("", "订单:" + str(order_sn_ysdk) + "状态不是请求cp发货成功", "fail")
    else:
        if order_re:
            report("", "order_re返回订单状态", "订单:"+str(order_sn)+"状态为通知cp成功")
        if order_re1:
            report("", "order_re1返回订单状态", "订单:"+str(order_sn_1)+"状态为通知cp成功")
        if order_re2:
            report("", "order_re2返回订单状态", "订单:"+str(order_sn_ysdk)+"状态为通知cp成功")
    return

def checktask():
    report("", "检查任务状态", "start")
    ck_re = False
    sql = ""
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='utf8')
    cur = conn.cursor()
    sql = "select * from run_log where task_id='" + task_id + "' and msg='fail'"
    cur.execute(sql)
    if int(cur.rowcount) == 0:
        ck_re = True
    cur.close()
    conn.close()
    report("", "检查任务状态" + str(ck_re), "end")
    return ck_re


def gettjdatastate():
    tj_active = 0
    tj_login = 0
    tj_order = 0
    analysis_id = ""
    t1 = datetime.datetime.now()
    t2 = t1 + datetime.timedelta(hours=-1)
    # t1=t1.strftime('%Y-%m-%d %H:%M:%S').replace(" ","%20")
    t1 = t1.strftime('%Y-%m-%d')
    t2 = t2.strftime('%Y-%m-%d %H:%M:%S').replace(" ", "%20")
    if game_xuhao > 62:
        analysis_id = game_channel_id
    else:
        analysis_id = str(channel_xuhao)

    # data_url="http://junhaidata-test.ijunhai.com/junhaiData/api/getAnaInfo?action_name=tjsdk&analysis_id="+analysis_id+"&time="+t1+"&device_id="+device_id
    # data_url="http://123.59.78.47:19200/logstash-jh-tj-sdk-*/_search?pretty&size=1000&q=device_id:%22"+device_id+"%22%20AND%20game_channel_id:%22"+analysis_id+"%22%20AND%20date:%22"+t1+"%22"
    data_url = "http://106.75.118.98:19200/logstash-jh-tj-sdk-*/_search?pretty&size=1000&q=device_id:%22" + device_id + "%22%20AND%20game_channel_id:%22" + analysis_id + "%22%20AND%20date:%22" + t1 + "%22"
    print(data_url)
    re = urlget(data_url)
    if re.find("ACTIVATION") > -1:
        tj_active = 1
    if re.find('LOGIN') > -1:
        tj_login = 1
    if re.find('"PAY') > -1:
        tj_order = 1
    '''
    if tj_active==0 or tj_login==0 or tj_order==0:
        #data_url="http://junhaidata-test.ijunhai.com/junhaiData/api/getAnaInfo?action_name=tjsdk&analysis_id="+analysis_id+"&time="+t2+"&device_id="+device_id
        data_url="http://123.59.78.47:19200/logstash-jh-tj-sdk-*/_search?pretty&size=1000&q=device_id:%22"+device_id+"%22%20AND%20game_channel_id:%"+analysis_id+"%22%20AND%20date:%"+t2+"%22"
        print(data_url)
        re=urlget(data_url)
        if re.find("ACTIVATION")>-1:
            tj_active=1
        if re.find('EVENTTAG":"LOGIN')>-1:
            tj_login=1
        if re.find('EVENTTAG":"PAY')>-1:
            tj_order=1
    '''
    if tj_active == 1 and tj_login == 1 and tj_order == 1:
        return True
    else:
        return False


def checkdata():
    report("tj_data", "检查数据", "start")
    k = 0
    if not checktask():
        report("tj_data", "任务有失败记录，执行2次查数据动作", "")
        # return
        k = 4

    global driver
    driver = ""

    data_re = False
    while k < 6 and not data_re:
        k = k + 1
        sleep(12 * k)
        data_re = gettjdatastate()
    if data_re:
        report("tj_data", "统计数据检查成功", "tcend")
        tcfenxi()
    else:
        report("", "检查统计数据失败", "fail")

def uninstall_app():
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='gbk')
    cur = conn.cursor()
    sql = "select * from task_testcase where task_id = '" + task_id + "' and state='失败'"
    try:
        cur.execute(sql)
        if int(cur.rowcount) > 0:
            print('有失败，不执行')
            report('','有失败不执行后面','')
            return ''
    except(Exception) as e:
        print(str(e))
    finally:
        cur.close()
        conn.close()
    report('','发包，卸载应用','')
    shell_set_app.uninstall_app(package,ud_id)


if __name__ == '__main__':
    
    print('success')
    suc()





