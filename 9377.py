# -*- coding: utf-8 -*-

import p
import unittest
import wda
from time import sleep
import sys
import opencv
import random


#task_id = '28340'
task_dir = '/Volumes/ntfs3-1/ios_python'

if len(sys.argv)>1:
    task_id=sys.argv[1]

p.setinfo(task_id)

def click_picture(screen_picture,current_picture,thing):
    global c
    global s
    c = wda.Client()
    s = c.session()
    p1 =  screen_picture
    p2 = current_picture
    a, x, y = opencv.imgcompare(p1, p2)
    k = 0
    while not a:
        c.screenshot(screen_picture)
        p1 = screen_picture
        p2 = current_picture
        a, x, y = opencv.imgcompare(p1, p2)
        k = k + 1
        print('尝试第', k, '次', thing)
        if k == 3:
            sleep(2)
            return False
    if a:
        print('截图 获取点击坐标', thing, a, x, y)
        p.touch(s, x, y)
        s.tap(x,y)
    return True


def find_picture(screen_picture,current_picture,thing):
    global c
    global s
    c = wda.Client()
    s = c.session()
    p1 =  screen_picture
    p2 = current_picture
    a, x, y = opencv.imgcompare(p1, p2)
    k = 0
    while not a:
        c.screenshot(screen_picture)
        p1 =  screen_picture
        p2 =  current_picture
        a, x, y = opencv.imgcompare(p1, p2)
        k = k + 1
        # 隔二秒再截图
        sleep(2)
        print('尝试第', k, '次', thing)
        if k == 4:
            return False
    if a:
        print('找图 获取点击坐标', thing, a, x, y)
    return True


def report(mo,msg):
    p.report('',mo,msg)

def update():

    sleep(3)
    # if click_picture(ima,'login.png','')
    p.report('','启动游戏更新','start')
    p.game('update')
    p.report('','启动游戏更新','tcend')
    p.tcfenxi()
    sleep(3)


def zhuce():
    print('9377 --------- zhuce')
    p.report('zhuce', '游戏快速注册', 'start')
    global c
    global s
    c = wda.Client()
    s = c.session()

    ss = s(name='快速注册登录').exists
    i = 0
    while not ss and i < 5:
        ss = s(name='快速注册登录').exists
        i += 1
        sleep(3)
    if ss:
        s(name='快速注册登录').get(3).click()
        p.report('zhuce', '游戏快速注册', 'tcend')
        sleep(2)
    sleep(3)
    
    
    ss = s(name='快速注册登陆').exists
    i = 0
    while not ss and i < 10:
        ss = s(name='快速注册登陆').exists
        i += 1
        sleep(3)
    if ss:
        s(name='快速注册登陆').get(3).click()
        p.report('zhuce', '游戏快速登陆', 'tcend')
        sleep(2)
    sleep(3)

    ss = s(name='一键登录').exists
    i = 0
    while not ss and i < 10:
        ss = s(name='一键登录').exists
        i += 1
        sleep(3)
    if ss:
        s(name='一键登录').get(3).click()
        p.report('zhuce', '一键登录', 'tcend')
        sleep(2)
    sleep(3)

    ss = s(name='登录').exists
    i = 0
    while not ss and i < 10:
        ss = s(name='登录').exists
        i += 1
        sleep(3)
    if ss:
        s(name='登录').get(3).click()
        p.report('zhuce', '登录', 'tcend')
        sleep(2)
    sleep(3)


    p.report('','游戏快速注册','end')

    #进入游戏
    #login()
    p.report('','调用游戏登录','start')
    p.game('login')
    p.report('', '调用游戏登录', 'end')



    return

def _alert_callback(session):
    print('call back------------------------------------------------------------------------------')
    session.alert.accept()


def login():
    print('9377 ----------- login')
    p.sessionstart()
    p.report('login','sdk登录','start')
    global c
    global s
    c = wda.Client()
    s = c.session()
    s.set_alert_callback(_alert_callback)
    ss = s(name='注册').exists

    i = 0
    while not ss and i < 10:
        ss = s(name='注册').exists
        i += 1
        sleep(3)

    if ss:
        s(name='注册').get(3).click()
        sleep(2)

    # 输入账号 第一种注册界面
    user = s(className='TextField', value='4个以上的字母或数字').exists
    if user:
        print('user')
        allz = 'abcdefghijklmnopqrstuvwxyz'
        allzlist = list(allz)
        username = random.sample(allzlist, 9)
        user_ku = ''
        for a in username:
            user_ku = user_ku + a
        print(user_ku)
        p.report('', '只测登录账号名字', str(user_ku))
        s(className='TextField', value='4个以上的字母或数字').set_text(username)
        sleep(1)
        s(name='隐藏键盘').get(timeout=3).click()
        sleep(3)

        pwd = s(className='SecureTextField', value='4个以上的字母或数字').exists
        if pwd:
            print('pwd')
            s(className='SecureTextField', value='4个以上的字母或数字').set_text('110110')
            p.report('', '只测登录账号密码', '110110')
            sleep(1)
            s(name='隐藏键盘').get(timeout=3).click()

        ss = s(name='完成注册').exists
        i = 0
        while not ss and i < 3:
            ss = s(name='完成注册').exists
            i += 1
            sleep(1)
        sleep(3)

        if ss:
            s(name='完成注册').get(3).click()
            sleep(2)
        sleep(3)
    '''
    #第二种注册账号界面，
    user = s(className='TextField', value='请输入账户').exists
    if user:
        allz = 'abcdefghijklmnopqrstuvwxyz'
        username = ''
        for x in range(8):
            username = username + random.choice(allz)
        p.report('','',username)
        s(className='TextField', value='请输入账户').set_text(username)
        sleep(1)
        s(name='隐藏键盘').get(timeout=3).click()
        sleep(1)

    '''



    ss = s(name='返回').exists
    i = 0
    while not ss and i < 3:
        ss = s(name='返回').exists
        i += 1
        sleep(3)

    if ss:
        s(name='返回').get(3).click()
        sleep(2)
    sleep(2)

    ss = s(name='登录').exists
    i = 0
    while not ss and i < 3:
        ss = s(name='登录').exists
        i += 1
        sleep(3)

    if ss:
        s(name='登录').get(3).click()
        sleep(2)
    sleep(3)

    #SDK信息
    p.report('login','调用游戏登录', 'start')
    p.game('login')
    p.report('login','调用游戏登录', 'end')
    p.report('','登录','end')
    return


def pay():
    global c
    global s
    c = wda.Client()
    s = c.session()
    p.checkweb1()
    p.report('pay','pay','start')
    p.report('','测试六元档','start')
    p.game('pay')
    p.report('','测试六元档','end')
    sleep(5)



    #p.checkweb()
    p.report('','订单','end')
    return




def report(mo,msg):
    p.report('',mo,msg)

def sessionquit():
    try:
        c.session().close()
    except(Exception) as e:
        print(str(e))
    return

class ContactsAndroidTests(unittest.TestCase):
    # driver=p.driver
    def setUp(self):
        # self.drvier=p.driverstart()
        sleep(1)
    
    
    def tearDown(self):
        p.tcfenxi()
        sessionquit()
    
    def test_2autologin_yueka(self):
        p.begin(task_id)
        p.tcfenxi()
        update()
        zhuce()
        p.tcfenxi()
        pay()
        p.tcfenxi()
        
        if p.checktask():
            #login()
            p.tcfenxi()

        p.checkweb()
        p.tcfenxi()
'''

class ContactsAndroidTests(unittest.TestCase):
    # driver=p.driver
    def setUp(self):
        # self.drvier=p.driverstart()
        sleep(1)


    def tearDown(self):
        p.tcfenxi()
        sessionquit()

    def test_2autologin_yueka(self):
        p.begin(task_id)
        p.tcfenxi()
        update()
        zhuce()
        p.tcfenxi()
        pay()
        p.tcfenxi()

    def test_3autologin_yueka(self):
        if p.checktask():
            #login()
            p.tcfenxi()

    def test_4autologin_yueka(self):
        sleep(10)
        p.checkweb()
        p.tcfenxi()
'''

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

