
import subprocess
import zipfile
import os
import unittest
import pymysql
import re
from biplist import *
from time import sleep

ip = "192.168.1.230"
xuqiu_id = ""
apk = ""

class SubTest():
    def runCmd(self,cmd):
        res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        sout,serr = res.communicate()
        return res.returncode,sout,serr

def get_deviceid(cmd='idevice_id -l'):
    st = SubTest()
    ret = st.runCmd(cmd)
    return ret[1].decode()

def get_devices(apk_path):
    if not os.path.exists(apk_path) or not zipfile.is_zipfile(apk_path):
        return None
    with zipfile.ZipFile(apk_path) as ipa:
        for file_name in ipa.namelist():
            search_str = '.app'
            index = file_name.find(search_str)
            if index != -1:
                info_plist_path = file_name[:index + len(search_str)] + '/embedded.mobileprovision'
                (f1, f2) = os.path.split(apk_path)
                expath = '/Volumes/apks/apks/mobile'
                ipa.extract(info_plist_path,path=expath)
                cmd = 'security cms -D -i ' + expath + '/' + info_plist_path
                res = get_deviceid(cmd)
                de = get_deviceid().strip()
                print(type(res),type(de))
                if res.find(de) > -1:
                    print('设备udid已经添加')
                    cmd = 'ideviceinstaller -i ' +apk_path+' -o ' + de
                    aa = get_deviceid(cmd)
                    print(aa)
                    return True
                print('设备udid没有添加')
                return False

def get_mobile(apk_path):
    if not os.path.exists(apk_path) or not zipfile.is_zipfile(apk_path):
        return None
    pres = ""
    with zipfile.ZipFile(apk_path) as ipa:
        for file_name in ipa.namelist():
            search_str = '.app'
            index = file_name.find(search_str)
            if index != -1:
                info_plist_path = file_name[:index + len(search_str)] + '/embedded.mobileprovision'
                (f1, f2) = os.path.split(apk_path)
                expath = '/Volumes/apks/apks/mobile'
                ipa.extract(info_plist_path,path=expath)
                cmd = 'security cms -D -i ' + expath + '/' + info_plist_path
                pres = get_deviceid(cmd)

                conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest',charset='utf8')
                cur = conn.cursor()

                try:
                    it = re.finditer(r'(<string>)(.){40}(</string>)', pres)
                    for i in it:
                        udid = i.group()
                        if udid.find('.') > -1:
                            continue
                        sql = "insert ipa_udid(xuqiu_list_id,udid,new_time) values('" + str(xuqiu_id) + "','" + str(udid) + "',now())"
                        cur.execute(sql)
                        conn.commit()
                    it = re.finditer(r'(<string>)(.){25}(</string>)', pres)
                    for i in it:
                        udid = i.group()
                        if udid.find('.') > -1:
                            continue
                        sql = "insert ipa_udid(xuqiu_list_id,udid,new_time) values('" + str(xuqiu_id) + "','" + udid + "',now())"
                        cur.execute(sql)
                        conn.commit()
                except(Exception) as e:
                    print(e)
                finally:
                    cur.close()
                    conn.close()
                    return None

def get_information(apk_path):
    if not os.path.exists(apk_path) or not zipfile.is_zipfile(apk_path):
        return None
    with zipfile.ZipFile(apk_path) as ipa:
        for file_name in ipa.namelist():
            search_str = '.app'
            index = file_name.find(search_str)
            if index != -1:
                info_plist_path = file_name[:index + len(search_str)] + '/Info.plist'
                info_dict = readPlistFromString(ipa.read(info_plist_path))
                game = info_dict['CFBundleDisplayName']
                package = info_dict['CFBundleIdentifier']
                version = info_dict['CFBundleShortVersionString']

                conn = pymysql.connect(host=ip, port=3306, user='root', passwd='password', db='autotest',charset='utf8')
                cur = conn.cursor()
                sql = "insert ipa_information(xuqiu_list_id,apk,game,package,version,new_time) values('"+str(xuqiu_id)+"','"+apk+"','"+game+"','"+package+"','"+version+"',now())"
                #print(sql)
                try:
                    cur.execute(sql)
                    conn.commit()
                except(Exception) as e:
                    print(str(e))
                finally:
                    cur.close()
                    conn.close()
                    return None


def get_ipa_udid():
    conn = pymysql.connect(host=ip, port=3306, user="root", passwd="password", db="autotest", charset="utf8")
    cur = conn.cursor()
    global xuqiu_id
    global apk
    xuqiu_id = ''
    apk = ''
    sql = "select id,apk from xuqiu_list where state='已提测' and location = '正版' and instr(apk,'ipa') and check_ipa = 1 order by id desc limit 1;"
    try:
        cur.execute(sql)
        for each in cur:
            xuqiu_id = each[0]
            apk = each[1]
            #print(xuqiu_id, apk)
    except(Exception) as e:
        print(e)
    if xuqiu_id == '' or apk == '' :
        print('没有符合条件的需求')
        cur.close()
        conn.close()
        return

    sql = "select path,get from waiwangtibao where wenjian = '"+apk+"' limit 1;"
    try:
        cur.execute(sql)
        for each in cur:
            apk_path = each[0]
            get = each[1]
            #print(apk_path)
    except(Exception) as e:
        print(e)
    finally:
        cur.close()
        conn.close()
    if apk.find('ipa') > -1:
        pass
    else:
        return
    if apk_path == "" or get == 0:
        return
    last = apk_path.split(":")[1]
    down_path = "/Volumes/apks" + last + apk

    #上传udid信息到ipa_udid表
    get_mobile(down_path)

    #上传包信息到ipa_information表
    get_information(down_path)


    #已经解忻过，标记一下
    try:
        conn = pymysql.connect(host=ip, port=3306, user="root", passwd="password", db="autotest", charset="utf8")
        cur = conn.cursor()
        sql = "update xuqiu_list set check_ipa = 2 where id ='"+str(xuqiu_id)+"' and location='正版';"
        print(sql)

    except(Exception) as e:
        print(e)
    finally:
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()


class ContactsAndroidTests(unittest.TestCase):
    # driver=p.driver
    def setUp(self):
        # self.drvier=p.driverstart()
        sleep(1)

    def tearDown(self):
        sleep(1)

    def test_1ipa(self):
        get_ipa_udid()
        sleep(5)



if __name__ == "__main__":
    #suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    a = 0
    while 1==1:
        a+=1
        if a == 3:
            pass
        print(a)
        try:

            get_ipa_udid()
            sleep(60)
        except(Exception) as e:
            print(e)
