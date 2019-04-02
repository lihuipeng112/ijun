# -*- coding: utf-8 -*-


from subprocess import Popen,PIPE
import os
import p
from time import sleep

def get_all_app():
    '''获取手机上所有的APP信息'''
    pp= Popen('ideviceinstaller -l',shell=True,stdout=PIPE,stderr=PIPE)
    p.report('','获取设备应用信息','')
    out,err = pp.communicate()
    out += err
    sleep(3)
    return out.decode()

def uninstall_app(bundle_id,ud_id):
    '''卸载APP'''
    cml = 'ideviceinstaller -u ' + ud_id + ' -U ' + bundle_id
    print(cml)
    pp= Popen(cml, shell=True, stdout=PIPE, stderr=PIPE)
    out,err = pp.communicate()
    out += err
    print('已经安装过，开始卸载')
    p.report('','检测到已经安装过','已经安装过，开始卸载')
    return out.decode()

def install_app(bundle_id_addredss,ud_id):
    '''安装APP'''
    print('开始安装----')
    p.report('','','开始安装')
    cml = 'ideviceinstaller -u ' + ud_id + ' -i ' + bundle_id_addredss
    pp= Popen(cml, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pp.communicate()
    out += err
    sleep(15)
    return out.decode()

def cmdrun(cmd):
    pp= Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pp.communicate()
    out += err
    return out


def set_app(bundle_id,ud_id,app_package):
    '''
    #安装打包APP
    :param bundle_id: 包名
    :param ud_id: 设备ID
    :param app_package: 安装文件名字
    :return:

    smb://192.168.1.225/apks/jzx/ymsj_dalan17_appstore_dis_v1.2.0(108)_20180103_1.ipa
        /Users/lichun/Documents/lihui

    '''
    if bundle_id == '':
        p.report('','包名为空','fail')
        return

    #bundle_id_address = os.path.join('/Volumes/ntfs3/ios_python', app_package)
    bundle_id_address = app_package
    #获取手机上所有的APP信息
    apps = get_all_app()
    p.report('','获取手机上所有app信息','')
    while bundle_id in apps:
        #如果手机上有这个APP包，先卸载
        u = uninstall_app(bundle_id,ud_id)
        print(u)
        apps = get_all_app()
        p.report('','','卸载成功')

    #安装
    install_app(bundle_id_address,ud_id)
    apps = get_all_app()
    if bundle_id in apps:
        #如果手机上有这个APP包，安装成功
        p.report('', '安装成功', 'end')
        return
    else:
        p.report('','安装失败','')
        p.report('','','fail')
        return

