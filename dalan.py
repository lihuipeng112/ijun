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
        p.report('',thing,i)
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
    print('dalan --------- zhuce')
    p.report('zhuce', '游戏注册', 'start')
    global c
    global s
    c = wda.Client()
    s = c.session()

    ss = s(name='同意并进入游戏').exists
    i = 0
    while not ss and i < 5:
        ss = s(name='同意并进入游戏').exists
        i += 1
        sleep(2)
    if ss:
        s(name='同意并进入游戏').get(3).click()
        p.report('zhuce', '同意并进入游戏', 'end')
        sleep(2)
    else:
        p.report('','没找到同意并进入游戏入口','')
    sleep(3)
    
    ss = s(name='进入游戏').exists
    i = 0
    while not ss and i < 5:
        ss = s(name='进入游戏').exists
        i += 1
        sleep(2)
    if ss:
        s(name='进入游戏').get(3).click()
        p.report('zhuce', '进入游戏', 'end')
        sleep(2)
    else:
        p.report('','没找到进入游戏入口','截图判断')
        click_picture(p.shot(),'/Volumes/ntfs3/ios_python/qudao/dalan_entergame.png','sdk截图判断进入游戏')
    sleep(3)

    #20180705新sdk用户协议
    if find_picture(p.shot(),'/Volumes/ntfs3/ios_python/qudao/dalanhuang.png','sdk截图判断进入游戏'):
        p.report('','新sdk','点击同意用户协议')
        click_picture(p.shot(),'/Volumes/ntfs3/ios_python/qudao/dalanhuang.png','sdk截图判断进入游戏')
    sleep(3)

    #20180705新sdk进入游戏
    enter_zhuce = find_picture(p.shot(),'/Volumes/ntfs3/ios_python/qudao/dalanhuang.png','sdk截图判断进入游戏')
    while not enter_zhuce and i < 3:
        enter_zhuce = find_picture(p.shot(),'/Volumes/ntfs3/ios_python/qudao/dalanhuang.png','sdk截图判断进入游戏')
        sleep(2)
        i += 1
        p.report('','新sdk','重新寻找进入游戏按钮')

    if enter_zhuce:
        click_picture(p.shot(),'/Volumes/ntfs3/ios_python/qudao/dalanhuang.png','sdk截图判断进入游戏')


    ss = s(name='好').exists
    i = 0
    while not ss and i < 5:
        ss = s(name='好').exists
        i += 1
        sleep(2)
    if ss:
        s(name='好').get(3).click()
        p.report('zhuce', '好', 'tcend')
        sleep(2)
    else:
        p.report('','没找到相册授权入口','')
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
    print('dalan ----------- login')
    sleep(3)
    p.sessionstart()
    p.report('login','sdk登录','start')
    global c
    global s
    c = wda.Client()
    s = c.session()
    #s.set_alert_callback(_alert_callback)
    
    sleep(5)
    #SDK信息
    p.report('login','调用游戏登录', 'start')
    p.game('autologin')
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
            login()
            p.tcfenxi()

        sleep(10)
        p.checkweb()
        p.tcfenxi()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

