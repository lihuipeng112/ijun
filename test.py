

import wda,opencv
from time import sleep
import p
from biplist import *
import os
import zipfile
import pymysql
import random

ip = '192.168.1.230'
global c
c = wda.Client()
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
        x = x+150
        p.touch(s, x, y)
        s.tap(x,y)
        print(x,y)
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
def alert_callback(session):
    btns = set([u'不再提醒', 'OK', u'知道了', 'Allow', u'允许']).intersection(session.alert.buttons())
    if len(btns) == 0:
        raise RuntimeError("Alert can not handled, buttons: " + ', '.join(session.alert.buttons()))
    session.alert.click(list(btns)[0])

def test1():

    c.screenshot('shot.png')
    el = find_picture('shot.png', '/Volumes/ntfs3/ios_python/jzx/allow.png', '查询是否要允许')
    #print(a)
    i = 0
    while el and i < 6:
        cl = click_picture('shot.png', '/Volumes/ntfs3/ios_python/jzx/allow.png', '查询是否要允许')
        if cl:
            print('出现权限允许')
            # p.report('update', '权限申请', '允许')
        else:
            sleep(3)
            el = find_picture('shot.png', '/Volumes/ntfs3/ios_python/jzx/allow.png', '查询是否要允许')
        i += 1

def test2():
    global c
    global s
    c = wda.Client()
    s = c.session()
    i = 0
    while i < 5:
        allow = s(name='允许').exists
        if allow:
            s(name='允许').get(timeout=3).click()
        i += 1
        sleep(3)
        print('查找允许第一次')

def test3():
    c.screenshot('shot.png')
    el = click_picture('shot.png', '/Volumes/ntfs3/ios_python/jzx/shantui.png', '闪退，我知道了')
    # print(a)
    nel = not el
    i = 0
    while nel and i < 6:
        cl = click_picture('shot.png', '/Volumes/ntfs3/ios_python/jzx/shantui.png', '闪退，我知道了')
        nel = not el
        sleep(3)
        i += 1

def zhuce():
    print('songshu --------- zhuce')
    global c
    global s
    c = wda.Client()
    s = c.session()
    ss = s(name='游客登录').exists

    i = 0
    while not ss and i < 10:
        ss = s(name='游客登录').exists
        i += 1
        sleep(3)

    if ss:
        s(name='游客登录').get(3).click()
        sleep(2)

        s(name='SS register protocol nomal@2x').get(3).click()
        sleep(2)
        s(name='游客登录').get(3).click()
        i += 1
    sleep(4)
    #出现权限，不允许
    allow = s(name = '不允许').exists
    if allow:
        s(name = '不允许').get(timeout=3).click()
        sleep(2)
    close = s(name ='SS close').exists
    if close:
        s(name='SS close').get(timeout=3).click()
        sleep(2)
def login():
    print('songshu ----------- login')
    #p.sessionstart()

    global c
    global s
    c = wda.Client()
    s = c.session()
    ss = s(name='立即登录').exists

    i = 0
    while not ss and i < 10:
        ss = s(name='立即登录').exists
        print('查找是否有sdk登录：%d' % i)
        i += 1
        sleep(3)

    if ss:
        s(name='立即登录').get(3).click()
        sleep(3)


    sb = s(name='稍后绑定').exists
    if sb:
        s(name='稍后绑定').get(3).click()
        sleep(2)

def get_ipa_game_channel_id(ipa_path):

    if not os.path.exists(ipa_path) or not zipfile.is_zipfile(ipa_path):
        print('get_info_none')
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
                print(game,package,version)

                conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest',
                                       charset='utf8')
                cur = conn.cursor()


                game1 = str(game)
                if game1.find('•')>-1:
                    print('有特殊字符，需要处理')
                    a1,a2 = game1.split('•')
                    print(a1,a2)
                    name = ''
                    sql = 'select game from task where id = 28340'
                    cur.execute(sql)
                    for each in cur:
                        name = each[0]
                    b1,b2 = name.split('?')
                    print(b1,b2)
                    if a1!=b1 or a2!=b2:
                        print('游戏不对')

                name = ''
                sql = 'select game from task where id = 28340'
                cur.execute(sql)
                for each in cur:
                    name = each[0]
                print(name)

                cur.close()
                conn.close()


                return False

def jiu_zhuce():
    print('9377 --------- zhuce')
    global c
    global s
    c = wda.Client()
    s = c.session('com.jhsfs.uwhd.shssj')
    ss = s(name='快速注册登录').exists

    i = 0
    while not ss and i < 10:
        ss = s(name='快速注册登录').exists
        i += 1
        sleep(3)

    if ss:
        s(name='快速注册登录').get(3).click()
        sleep(2)

    sleep(3)

    print('调用游戏登录')
def jiu_login():
    print('9377 --------- login')
    global c
    global s
    c = wda.Client()
    s = c.session('com.jhsfs.uwhd.shssj')
    ss = s(name='注册').exists

    i = 0
    while not ss and i < 10:
        ss = s(name='注册').exists
        i += 1
        sleep(3)

    if ss:
        s(name='注册').get(3).click()
        sleep(2)

    #输入账号
    user = s(className='TextField',value='4个以上的字母或数字').exists
    if user:
        print('user')
        allz = 'abcdefghijklmnopqrstuvwxyz'
        allzlist = list(allz)
        username = random.sample(allzlist, 9)
        s(className='TextField', value='4个以上的字母或数字').set_text(username)
        sleep(1)
        s(name='隐藏键盘').get(timeout=3).click()
        sleep(3)
    pwd = s(className='SecureTextField',value='4个以上的字母或数字').exists
    if pwd:
        print('pwd')
        s(className='SecureTextField', value='4个以上的字母或数字').set_text('110110')
        sleep(1)
        s(name='隐藏键盘').get(timeout=3).click()

    ss = s(name='完成注册').exists
    i = 0
    while not ss and i < 3:
        ss = s(name='完成注册').exists
        i += 1
        sleep(3)

    if ss:
        s(name='完成注册').get(3).click()
        sleep(2)
    sleep(3)
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

    print('调用游戏登录')

def jing_zhuce():
    print('jzx --- zhuce')
    #p.report('zhuce', '快速注册账号', 'start')
    global c
    global s
    c = wda.Client()
    s = c.session('qmgjxy.cyhd')

    ss = s(name='快速注册').exists
    i = 0
    while not ss and i < 10:
        ss = s(name='快速注册').exists
        i += 1
        sleep(3)

    if ss:
        s(name='快速注册').get(3).click()
        sleep(2)

    ss = s(name='注册').exists
    i = 0
    while not ss and i < 10:
        ss = s(name='注册').exists
        i += 1
        sleep(3)

    if ss:
        s(name='注册').get(3).click()
        p.report('', '快速注册账号', 'tcend')
        sleep(2)
    else:
        # 如果没有找到注册按钮，证明没有进入快速注册界面，注册失败
        #p.report('', '快速注册账号', 'fail')
        return
    #p.report('', '游戏快速注册', 'end')
    print('jzx --- zhuce')
    return


def jing_login():
    print('jingdian --------- login')
    global c
    global s
    c = wda.Client()
    s = c.session('qmgjxy.cyhd')

    ss = s(name='登录').exists
    i = 0
    while not ss and i < 10:
        ss = s(name='登录').exists
        i += 1
        sleep(3)

    if ss:
        s(name='登录').get(3).click()
        sleep(2)



def get_ipa_game_channel_id(ipa_path):

    if not os.path.exists(ipa_path) or not zipfile.is_zipfile(ipa_path):
        print('get_info_none')
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
                try:

                    game_channel_id=info_dict.get('junhaiChannel').get('gameChannelId')
                    print('game_channel_id:',game_channel_id)
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
                    
def enc():
    task_id = 32603
    conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest', charset='utf8')
    cur = conn.cursor()
    # 从task表中读取任务信息
    sql = "select t.id,t.device,t.package,t.activity,t.game_exe,t.apk,t.yueka_price,t.yueka_name,t.shiyuan_price,t.shiyuan_name,t.channel_id,t.game_id,d.name,d.ip,t.game,d.udid from task t,device d where t.id = '%s' and t.device = d.device" % task_id
    cur.execute(sql)
    for each in cur:

        device = each[1]
        device0 = device
        package = each[2]
        print(device, package)
    print(device,package)

def begin(task_id):
    global c
    c = wda.Client()
    c.home()
    p.suc()

def get_ipa(ipa_path):

    if not os.path.exists(ipa_path) or not zipfile.is_zipfile(ipa_path):
        print('get_info_none')
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
                #info_dict = convert(info_dict)
                game=info_dict[b'CFBundleDisplayName']
                package=info_dict[b'CFBundleIdentifier']
                version=info_dict[b'CFBundleShortVersionString']
        game = convert(game)
        package = convert(package)
        version = convert(version)
        print(game,package,version)
def convert(data):
    '''

    :param data: 传入一个字典
    :return: 将非字典中的非字符串，转化为字符串
    '''
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data


if __name__ =='__main__':
    get_ipa('9377.ipa')
