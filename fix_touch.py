
import os,sys
from subprocess import Popen,PIPE

def touch(session, x, y):
    if session.orientation == 'LANDSCAPE':
        window_size = session.window_size()
        fix_x = y
        fix_y = window_size.height - x
    else:
        fix_x = x
        fix_y = y
    session.tap(fix_x, fix_y)


def cmdrun(cmd):
    p = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)
    out,err = p.communicate()
    out +=err
    return out

def bundle1():
    f = open('install.txt','r')
    a = f.read()
    b1 = a.index('Installing')
    b2 = a.index('-')
    c = a[b1:b2]
    r = c.replace('Installing ','').replace("'","").strip()
    f.close()
    #r = 'com.dalan.qyz.appstore'
    return r
    

