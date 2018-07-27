# -*- coding: utf-8 -*-
import wda
import opencv
import p
from time import sleep
import ps

global c
global s
c = wda.Client()
s = c.session()
task_dir = '/Users/lichun/Documents/lihui/'

#对比图片
def click_picture(screen_picture,current_picture,thing):
    p1 =  screen_picture
    p2 = current_picture
    print(s.window_size())
    print(p1)
    print(p2)
    a, x, y = opencv.imgcompare(p1, p2)
    k = 0
    while not a:
        c.screenshot(screen_picture)
        p1 =  screen_picture
        p2 =  current_picture
        a, x, y = opencv.imgcompare(p1, p2)
        k = k + 1
        # 隔一秒再截图
        sleep(1)
        print('截图  尝试第', k, '次', thing)
        if k == 3:
            return False
    if a:
        print('click获取点击坐标', thing, a, x, y)
        s().wait(1.0)
        #p.touch(s, x, y)
        s.tap(x,y)
    return True

def find_picture(screen_picture,current_picture,thing):
    p1 =  screen_picture
    p2 = current_picture
    print(s.window_size())
    print(p1)
    print(p2)
    a, x, y = opencv.imgcompare(p1, p2)
    k = 0
    while not a:
        c.screenshot(screen_picture)
        p1 =  screen_picture
        p2 =  current_picture
        a, x, y = opencv.imgcompare(p1, p2)
        k = k + 1
        # 隔一秒再截图
        sleep(1)
        print('找图  尝试第', k, '次', thing)
        if k == 3:
            return False
    if a:
        print('find获取点击坐标', thing, a, x, y)
    return True

def find_picture1(screen_picture,current_picture,thing):
    p1 = screen_picture
    p2 = current_picture
    print(s.window_size())
    print(p1)
    print(p2)
    a, x, y = opencv.imgcompare(p1, p2)
    k = 0
    while not a:
        c.screenshot(screen_picture)
        p1 =  screen_picture
        p2 =  current_picture
        a, x, y = opencv.imgcompare(p1, p2)
        k = k + 1
        # 隔15秒再截图
        sleep(15)
        print('找图1  尝试第', k, '次', thing)
        if k == 4:
            return False
    if a:
        print('find获取点击坐标', thing, a, x, y)
    return True

def autologin():
    p.report('', '游戏登录', 'start')
    global c
    global s
    c = wda.Client()
    s = c.session()
    sleep(3)

    click_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/kaishiyouxi.png','开始游戏')

    newj = find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/jinruyouxi.png', '进入游戏')
    if newj:
        click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/jinruyouxi.png', '进入游戏')


    game = not find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/chongzhi.png', '游戏界面')
    i = 0
    while game and i < 3:
        s.tap(330,50)
        i += 1
        game = not find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/chongzhi.png', '游戏界面')
    if not game:
        p.report('','登录游戏','tcend')
    sleep(5)
    p.shot()

def login():
    p.report('','游戏登录','start')
    global c
    global s
    c = wda.Client()
    s = c.session()
    sleep(3)
    #国行第一次会进行无网优化
    #click_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/kaishiyouxi.png','我知道了')

    #sleep(3)
    #p.sessionstart()
    #登录游戏
    #判断，正常情况下创建新账号的流程是：开始游戏 -> 创建角色，接着进入游戏
    #正常情况下登录已经有角色账号的流程是：开始游戏 -> 进入游戏，接着进入游戏，进行判断，如果没有创建角色按钮，再判断是否有进入游戏


    # 开始游戏 创建角色 游戏界面 （忽略重名的情况）
    click_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/kaishiyouxi.png','开始游戏')

    i = 0
    new1 = find_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/newjuese.png','创建角色')
    p.report('','查找是否有判断角色',new1)
    in1 = find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/jinruyouxi.png', '进入游戏')
    p.report('', '查找是否有进入游戏', in1)
    while not new1 and not in1 and i < 3:
        click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/kaishiyouxi.png', '开始游戏')
        new1 = find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/newjuese.png', '创建角色')
        in1 = find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/jinruyouxi.png', '进入游戏')
        i += 1
        p.report('','在登录界面判断',i)
    newj = find_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/newjuese.png','创建角色')
    if newj:
        p.report('','点击创建角色','')
        click_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/newjuese.png','创建角色')


    game = True
    if find_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/chongzhi.png','游戏界面'):
        sleep(4)
        p.shot()
        print('11进入游戏成功')
        p.report('', '注册登录游戏', 'tcend')
        s.tap(330, 50)
        game = False

    # 开始游戏 进入游戏 游戏界面
    if game:
        newj = find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/jinruyouxi.png', '进入游戏')
        if newj:
            p.report('', '进入游戏', '')
            click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/jinruyouxi.png', '进入游戏')
    game = not find_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/chongzhi.png','游戏界面')
    # 开始游戏 创建角色 游戏界面 （重名的情况,随机五次，已经进入游戏，不会执行）
    j = 0
    while game and j < 5:
        p.report('','角色重名，重新扔骰子',j)
        click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/randomname.png', '点击骰子')
        sleep(1)
        click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/newjuese.png', '创建角色')
        j += 1
        game = not find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/chongzhi.png', '游戏界面')
        if game == False:
            print('22进入游戏成功')
            sleep(4)
            p.shot()
            p.report('','注册登录游戏','tcend')
            s.tap(330, 50)
    s.tap(330, 50)
    if find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/chongzhi.png', '游戏界面'):
        p.report('','','tcend')


def replace_server(newT,baginT):
    global c
    global s
    c = wda.Client()
    s = c.session()
    if not newT and not baginT:
        #没有进入游戏，服务器有问题，更换服务器
        if click_picture(p.shot(),'/Users/lichun/Documents/lihui/bingxue/sever_replace.png','更换服务器'):
            if click_picture(p.shot(),'/Users/lichun/Documents/lihui/bingxue/sever_new.png','点击新服'):
                pass
        else:
            print('没有服务器')
            p.report('','','没有服务器')




def pay2():
    print('jzx---------------------pay')
    #打开首充界面
    p.report('','游戏6元','start')
    #sleep(2)
    s.tap(330, 50)
    #防止触发任务，在游戏中上方点击下
    i = 0
    while not find_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/chongzhi.png','打开充值界面') and i < 4:
        p.report('', '', '点击一下屏幕')
        s.tap(330,50)
        i += 1
        sleep(1)
    sleep(1)
    s.tap(330, 50)
    #正常支付流程   打开充值-点击6元档-支付
    if click_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/chongzhi.png','打开充值界面'):
        #p.report('','游戏主界面','打开充值界面')
        i = 0
        while click_picture(p.shot(),'/Volumes/ntfs3/ios_python/jzx/jzx_six.png','点击六元档') and i < 3:
            p.report('','充值界面','打开六元充值档')
            #apple支付判断界面
            user = 'dongxiaoTest@163.com'
            pwd = 'Dongxiao123'
            pay_end = ps.apple_pay(c.session(), user, pwd)
            if pay_end == True:
                print('支付成功')
                p.report('pay','游戏6元','end')
                break
            elif pay_end == 2:
                print('需要重新点击6元档')

            elif pay_end == 3:
                #输入账号密码之后，如果超时，1、等待超时，重新购买 2、沙箱账号问题
                print('等待确认输入框超时，重新购买')

            else:
                print('其它情况')
            i += 1


def pay():
    print('jzx---------------------pay')
    # 打开首充界面
    p.report('', '游戏6元', 'start')
    sleep(5)
    s.tap(330, 50)
    p.report('', '点击屏幕上方', '')
    # 防止触发任务，在游戏中上方点击下
    i = 0
    fc = find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/chongzhi.png', '打开充值界面')
    while not fc and i < 4:
        s.tap(330, 50)
        sleep(1)
        i += 1
        p.report('', '没找到充值按钮', i)
        fc = find_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/chongzhi.png', '打开充值界面')
    # 正常支付流程   打开充值-点击6元档-支付
    sleep(1)
    if click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/chongzhi.png', '打开充值界面'):
        # p.report('','游戏主界面','打开充值界面')
        pay_end = False
        i = 0
        while click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/jzx_six.png', '点击六元档') and i < 3:
            p.report('', '充值界面', '打开六元充值档')
            # apple支付判断界面
            user = 'xcwc123@163.com'
            pwd = 'Aa11223344'
            user = p.account
            pwd = p.password
            user = user.strip()
            pwd = pwd.strip()
            pay_end = ps.apple_pay(c.session(), user, pwd)
            if pay_end == True:
                #苹果支付成功，并查询到到账金额是60元宝，则支付成功
                print('支付成功')
                dz = find_picture1(p.shot(), '/Volumes/ntfs3/ios_python/jzx/buy_daozhang.png','购买到账')
                if dz:
                    p.shot()
                    p.report('','到账成功','60元宝')
                    print('到账成功')
                    p.report('pay', '游戏6元', 'tcend')
                break
            i += 1

        if pay_end == False:
            p.shot()
            print('支付失败')
            p.report('pay', '游戏6元', 'fail')


def update():
    p.report('update', '更新', 'start')
    global s
    global c
    #s = p.sessionstart()

    # s.set_alert_callback(_alert_callback)
    sleep(2)

    # 查找权限允许
    i = 0
    while i < 5:
        allow = s(name='允许').exists
        if allow:
            s(name='允许').get(timeout=3).click()
            p.shot()
        allow = s(name='好').exists
        if allow:
            s(name='好').get(timeout=3).click()
            p.shot()
        allow = s(name='确定').exists
        if allow:
            s(name='确定').get(timeout=3).click()
            p.shot()
        i += 1
        sleep(3)
        p.report('', '权限允许查询', '第%d次' % i)

    el = click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/shantui.png', '闪退，我知道了')
    # print(a)
    if el:
        p.report('', '优化闪退', '退出重进')
        p.sessionstart()

    nel = not el
    i = 0
    while nel and i < 2:
        el = click_picture(p.shot(), '/Volumes/ntfs3/ios_python/jzx/shantui.png', '闪退，我知道了')
        if el:
            p.report('', '优化闪退', '退出重进')
            p.sessionstart()
        nel = not el
        sleep(3)
        p.report('', '查找闪退图', '第%d次' % i)
        i += 1



if __name__ =='__main__':
    c.screenshot('shot.png')
    ok = find_picture1('/Volumes/ntfs3/ios_python/shot.png','/Volumes/ntfs3/ios_python/jzx/buy_daozhang.png','购买60元到账')
    if ok:
        print(ok)
    else:
        print('没找到')







