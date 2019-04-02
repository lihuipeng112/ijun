
import opencv
import wda
from time import sleep
import shell_set_app
import random
import p

def clear_appitunes():
    '''
    清除APP账号
    '''
    global c
    c = wda.Client()
    #report('', 'setting', '配置账号信息')
    with c.session('com.apple.Preferences') as s:
        m1 = s(name='设置').exists
        if m1:
            print('打开设置')
            s(name='设置').get(timeout=10).tap()
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



def click_picture(screen_picture,current_picture,thing):
    global c
    global s
    c = wda.Client()
    s = c.session()
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
        # 隔二秒再截图
        sleep(2)
        print('截图  尝试第', k, '次', thing)
        if k == 10:
            return False
    if a:
        print('获取点击坐标', thing, a, x, y)
        s().wait(1.0)
        #p.touch(s, x, y)
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
        print('截图  尝试第', k, '次', thing)
        if k == 10:
            return False
    if a:
        print('获取点击坐标', thing, a, x, y)
    return True

#支付方式--截图判断
def pay(appuser,apppwd):
    global c
    global s
    c = wda.Client()
    s = c.session()

    #来这里调用苹果支付，并返回

    # 打开现有的apple账号
    if click_picture(c.screenshot('shot.png'), '/Users/lichun/Documents/lihui/ps/useappleid.png', '使用现有的apple id'):
        e = s(value='example@icloud.com')
        if e.exists:

            e.get(timeout=5).set_text(appuser)
            s(value='密码').get(timeout=3).set_text(apppwd)
        s(name='购买').get(timeout=3).tap()
        # 等待网络延时
        if find_picture(c.screenshot('shot.png'), '/Users/lichun/Documents/lihui/ps/buysure.png', '确认购买'):
            if s(value='请确认您的 App 内购买项目').exists:
                # 购买
                print('yes')
                s(name='购买').get(timeout=3).tap()
                # 判断是否有弹出购买完成
                if find_picture(c.screenshot('shot.png'), '/Users/lichun/Documents/lihui/jzx/buyend.png', '购买完成'):
                    s(name='好').get(timeout=3).tap()

def test():
    global c
    global s
    c = wda.Client()
    s = c.session('com.xyxyj')
    sleep(3)
    s(name='立即登录').get(5).click()
    sleep(3)
    s(name='稍后绑定').get(5).click()
    sleep(2)

    click_picture('shot.png','/Users/lichun/Documents/lihui/jzx/jzx_begin.png','开始游戏')
    click_picture('shot.png','/Users/lichun/Documents/lihui/jzx/jzx_enter.png','进入游戏')
    click_picture('shot.png','/Users/lichun/Documents/lihui/jzx/chongzhi.png','充值开始')
    click_picture('shot.png', '/Users/lichun/Documents/lihui/jzx/jzx_six.png', '充值6元')

    #调用apple支付处理
    userid = '21845315812@qq.com'
    userpwd = 'Zouziwen102'
    apple_pay(s,userid,userpwd)

    buy_end = click_picture('shot.png','/Users/lichun/Documents/lihui/jzx/buyknow.png', '我知道了')
    if buy_end:
        tcfenxi()

def tcfenxi():
    print('start fenxi')


#支付方式--控件判断
def apple_pay(s,userid,userpwd):
    print('ps----------------------apple_pay')
    s.set_alert_callback(_alert_callback)
    print('apple_pay being')

    id_wait = s(name='使用现有的 Apple ID')
    i = 0
    while not id_wait.exists:
        sleep(5)
        id_wait = s(name='使用现有的 Apple ID')
        i += 1
        print('第%d次寻找是否弹出了账号输入'% i)
        p.report('','','第%d次寻找是否弹出了账号输入'% i)
        if i == 15:
            #没有找到账号输入，证明需要重新点击
            return False

    #输入账号密码
    if id_wait.exists:
        id_wait.get(5).click()
        sleep(4)
        e = s(value='example@icloud.com')
        if e.exists:
            e.get(timeout=5).set_text(userid)
            s(value='密码').get(timeout=3).set_text(userpwd)
            p.shot()
            s(name='购买').get(timeout=3).tap()

    buy_wait = s(name='购买')
    #确认购买
    i = 0
    while not buy_wait.exists:
        sleep(5)
        buy_wait = s(name='购买')
        i += 1
        print('第%d次寻找是否弹出了购买确认' % i)
        p.report('', '', '第%d次寻找是否弹出了购买确认' % i)
        if i == 15:
            #确认购买框还没有出来，重新购买
            return False
    if buy_wait.exists:
        sleep(3)
        p.shot()
        buy_wait.get(5).click()

    sleep(3)
    sure_wait = s(name='好')
    i = 0
    while not sure_wait.exists and i < 15:
        sleep(5)
        sure_wait = s(name='好')
        i += 1
        print('第%d次寻找是否弹出了购买完毕' % i)
    if sure_wait.exists:
        p.shot()
        sure_wait.get(5).click()
        return True

def pay_again(s,userid,userpwd):
    id_wait = s(name='重试')
    i = 0
    while not id_wait.exists and i < 10:
        sleep(4)
        id_wait = s(name='重试')
        i += 1
        print('第%d次寻找是否弹出了账号输入' % i)
        if i == 10:
            # 没有找到账号输入，证明需要重新点击
            return False

    apple_pay(s, userid, userpwd)


def test_zhuce():
    print('zhuce------------------------------------------------------------------------------')
    global c
    global s
    c = wda.Client()
    s = c.session('com.xyxyj')

    s.set_alert_callback(_alert_callback)

    s(name='SS register').get(3).click()
    sleep(2)
    allz = 'abcdefghijklmnopqrstuvwxyz'
    allzlist = list(allz)
    username = random.sample(allzlist, 9)
    s(name='一键注册').get(3).click()
    sleep(2)
    s(name='SS close').get(3).click()


    click_picture('shot.png', '/Users/lichun/Documents/lihui/jzx/jzx_begin.png', '开始游戏')
    click_picture('shot.png', '/Users/lichun/Documents/lihui/jzx/chuangjianjuese.png', '创建角色')
    sleep(6)
    # 防止触发任务，在游戏中上方点击下
    s.tap(330, 50)
    click_picture('shot.png', '/Users/lichun/Documents/lihui/jzx/chongzhi.png', '充值开始')
    click_picture('shot.png', '/Users/lichun/Documents/lihui/jzx/jzx_six.png', '充值6元')

    # 调用apple支付处理
    userid = '21845315812@qq.com'
    userpwd = 'Zouziwen102'
    apple_pay(s, userid, userpwd)

    buy_end = click_picture('shot.png', '/Users/lichun/Documents/lihui/jzx/buyknow.png', '我知道了')
    if buy_end:
        tcfenxi()

def _alert_callback(session):
    print('call back------------------------------------------------------------------------------')
    session.alert.accept()

if __name__ == '__main__':
    clear_appitunes()
    shell_set_app.set_app('com.xyxyj','770a083e28d146f995fc75cbc804bd4dc0845ffd','xyxyj.ipa')
    test_zhuce()












