# -*- coding: utf-8 -*-

import p
import unittest
import wda
from time import sleep
import sys
import opencv
import random


#task_id = '28340'
task_dir = '/Volumes/ntfs3/ios_python'
username = ''
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
    print('zhangkun --------- zhuce')
    p.report('zhuce', '掌昆游戏注册', 'start')
    global c
    global s
    c = wda.Client()
    s = c.session()

    ss = s(name='立即注册').exists
    i = 0
    while not ss and i < 5:
        ss = s(name='立即注册').exists
        p.report('', '查找注册接口', i)
        i += 1
        sleep(2)
    if ss:
        s(name='立即注册').get(3).click()
        p.report('zhuce', '立即注册', '')
        sleep(2)
    sleep(3)

    ss = s(name='好').exists
    i = 0
    while not ss and i < 5:
        ss = s(name='好').exists
        i += 1
        sleep(2)
    if ss:
        s(name='好').get(3).click()
        p.report('zhuce', '好', '')
        sleep(2)
    sleep(3)

    ss = s(name='close button').exists
    i = 0
    while not ss and i < 5:
        ss = s(name='close button').exists
        i += 1
        sleep(2)
    if ss:
        s(name='close button').get(3).click()
        p.report('zhuce', '关掉手机绑定', '')
        sleep(2)
    sleep(3)
    #进入游戏
    #login()
    p.report('','调用游戏登录','start')
    p.game('login')
    s.close()
    p.report('', '调用游戏登录', 'end')
    return

def zhuce_my():
    print('zhangkun --------- zhuce')
    p.report('zhuce_my', '开始', '')
    p.sessionstart()
    global c
    global s
    global username
    c = wda.Client()
    s = c.session()
    s.set_alert_callback(_alert_callback)

    ss = s(name='账号注册').exists
    p.report('','首次查找账号注册','')
    sleep(2)
    i = 0
    while not ss and i < 5:
        ss = s(name='账号注册').exists
        i += 1
        sleep(2)
    if ss:
        p.report('','点击账号注册','')
        s(name='账号注册').get(3).click()
        sleep(2)
    sleep(3)

    # 输入账号
    user = s(className='TextField', value='6-20位数字或字母').exists
    if user:
        print('user')
        allz = 'abcdefghijklmnopqrstuvwxyz123456789abcdefghijklmnopqrstuvwxyz123456789'
        allzlist = list(allz)
        username = random.sample(allzlist, 12)
        user_ku = ''
        for a in username:
            user_ku = user_ku + a
        print(user_ku)
        s(className='TextField', value='6-20位数字或字母').set_text(username)
        p.report('','账号注册账号',user_ku)
        p.report('zhuce_my', '立即注册', '')
        sleep(3)
        s(name='隐藏键盘').get(timeout=3).click()
        sleep(2)
        p.report('', '隐藏账号键盘', '')
    pwd = s(className='TextField', value='6-20位数字或字母').exists
    if pwd:
        print('pwd')
        s(className='TextField', value='6-20位数字或字母').set_text('110110')
        p.report('','点击账号密码','110110')
        sleep(1)
        s(name='隐藏键盘').get(timeout=3).click()
        sleep(2)
        p.report('','隐藏密码键盘','')
        sleep(1)

    ss = s(name='立即注册').exists
    sleep(2)
    i = 0
    while not ss and i < 5:
        ss = s(name='立即注册').exists
        i += 1
        p.report('', '查找立即注册按钮', i)
        sleep(2)

    if ss:
        p.shot()
        sleep(2)
        s(name='立即注册').get(3).click()
        p.report('', '注册账号成功', '')
        sleep(2)
    sleep(3)

    ss = s(name='close button').exists
    sleep(2)
    i = 0
    while not ss and i < 5:
        ss = s(name='close button').exists
        i += 1
        sleep(2)
    if ss:
        s(name='close button').get(3).click()
        sleep(2)
    sleep(3)

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
    print('zhangkun --------- zhuce')
    p.report('login','调用sdk登录','start')
    p.sessionstart()
    global c
    global s
    c = wda.Client()
    s = c.session()
    
    ss = s(name='账号登录').exists
    sleep(3)
    i = 0
    while not ss and i < 5:
        ss = s(name='账号登录').exists
        i += 1
        sleep(2)
    if ss:
        s(name='账号登录').get(3).click()
        p.report('','点击账号登录','')
        sleep(2)
    sleep(3)

    # 输入账号
    user = s(className='TextField', value='输入帐号/手机号').exists
    if user:
        #username='lihuipeng112'
        s(className='TextField', value='输入帐号/手机号').set_text(username)
        p.report('','输入账号','')
        sleep(3)
        s(name='隐藏键盘').get(timeout=3).click()

    pwd = s(className='TextField', value='输入密码').exists
    if pwd:
        print('pwd')
        s(className='TextField', value='输入密码').set_text('110110')
        p.report('','输入密码','')
        sleep(1)
        s(name='隐藏键盘').get(timeout=3).click()

    ss = s(name='进入游戏').exists
    sleep(3)
    i = 0
    while not ss and i < 5:
        ss = s(name='进入游戏').exists
        i += 1
        sleep(2)
    if ss:
        p.shot()
        s(name='进入游戏').get(3).click()
        sleep(2)
        p.report('','进入游戏','')
    sleep(3)

    ss = s(name='close button').exists
    i = 0
    while not ss and i < 5:
        ss = s(name='close button').exists
        i += 1
        sleep(2)
    if ss:
        s(name='close button').get(3).click()
        sleep(2)
    sleep(3)



    #SDK信息
    p.report('','调用游戏登录', 'start')
    p.game('autologin')
    p.report('','调用游戏登录', 'end')
    p.report('','登录','end')
    
    return


def pay():

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
        #zhuce()
        p.tcfenxi()
        zhuce_my()
        p.tcfenxi()
        pay()
        p.tcfenxi()

        sleep(5)
        login()
        p.tcfenxi()

        sleep(10)
        p.checkweb()
        p.tcfenxi()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

