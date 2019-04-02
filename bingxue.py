# -*- coding: utf-8 -*-

import p
import unittest
import wda
from time import sleep
import sys
import opencv
import random


task_id = '10062'
task_dir = '/Users/lichun/Documents/lihu'

if len(sys.argv)>1:
    task_id=sys.argv[1]

p.setinfo(task_id)

def find_picture(screen_picture,current_picture,thing):
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
        if k == 10:
            return False
    if a:
        print('获取点击坐标', thing, a, x, y)
    return True


def report(mo,msg):
    p.report('',mo,msg)

def update():
    p.report('','sdk游戏更新','start')
    print(p.task_id)
    p.report1('','update','截图')
    sleep(5)
    aa = p.shot()
    if click_picture(aa, '/Users/lichun/Documents/lihui/bingxue/allow.png', '查询是否要允许'):
        p.report('', '允许发送通知', 'update')
    sleep(3)
    # if click_picture(ima,'login.png','')

def zhuce():
    global c
    global s
    c = wda.Client()
    s = c.session()
    p.report('zhuce','','注册新账号')
    if click_picture(p.shot(),'/Users/lichun/Documents/lihui/bingxue/register.png','自定义注册账号'):
        p.report('zhuce','注册新账号','')
        if click_picture(p.shot(),'/Users/lichun/Documents/lihui/bingxue/user.png','输入账号'):
            allz = 'abcdefghijklmnopqrstuvwxyz'
            allzlist = list(allz)
            username = random.sample(allzlist, 9)
            s(name='L').get(timeout=3).tap()
            for a in username:
                s(name=a).get(timeout=3).tap()
            p.report('zhuce','账号',''.join(username))
            p.report('zhuce','密码','qqqqqqq')
            s(name='Next:').get(timeout=4).tap()
            #密码7个q
            for i in range(7):
                s(name='q').get(timeout=3).tap()
            s(name='Next:').get(timeout=4).tap()
            #确认密码
            for i in range(7):
                s(name='q').get(timeout=3).tap()
            s(name='Done').get(timeout=4).tap()
        sleep(1)
        if click_picture(p.shot(),'/Users/lichun/Documents/lihui/bingxue/register_success.png','输入账号信息准备进入游戏'):
            print('success')
            #绑定手机号
            if click_picture(p.shot(),'/Users/lichun/Documents/lihui/bingxue/after.png','稍后绑定'):
                print('准备进入游戏')
                report('绑定手机号','取消')
            else:
                report('没有找到绑定手机号界面','')
    #进入游戏
    login()
    return

def shiyuan():
    global c
    global s
    c = wda.Client()
    s = c.session()

    p.report('shiyuan','shiyuan','start')
    p.report('','调用游戏充值','start')
    p.game('shiyuan')
    p.report('','调用游戏充值','end')
    sleep(5)

    #等待是否出现APPle输入账号界面,相当于判断是否会进入到订单界面
    find_picture(p.shot(), '/Users/lichun/Documents/lihui/jzx/buysure.png', '确认购买')
    dot = 0
    while not e.exists:
        dot += 1
        if dot > 10:
            p.report('','等待订单出现界面超时','fail')
            report()
        sleep(5)
        p.report('','等待订单界面出现','等待中')
        e = s(name='使用现有的 Apple ID')

    #已经有输入账号界面了



def login():
    #出现权限允许
    if click_picture(p.shot(), '/Users/lichun/Documents/lihui/bingxue/allow.png', '查询是否要允许'):
        p.report('', '允许发送通知', 'update')
    #SDK信息
    report('调用游戏登录', 'start')
    p.game('login')
    report('调用游戏登录', 'end')

    p.report('','登录','tcend')
    return


def pay():
    global c
    global s
    c = wda.Client()
    s = c.session()

    p.report('pay','pay','start')
    p.report('','测试六元档','start')
    p.game('pay')
    p.report('','测试六元档','end')
    sleep(5)




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
        if k == 10:
            sleep(1)
            return False
    if a:
        print('获取点击坐标', thing, a, x, y)
        p.touch(s, x, y)
        s.tap(x,y)
    return True


def report(mo,msg):
    p.report('',mo,msg)


if __name__ == '__main__':

    p.begin(task_id)
    update()
    zhuce()
    p.tcfenxi()
    pay()

    p.tcfenxi()
    p.sessionquit()
