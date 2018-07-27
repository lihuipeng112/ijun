# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 16:10:33 2014
@author: duan
"""
import os
import sys
import cv2
import numpy as np
def imgcompare(i1,i2,*xs):
    #print(i1+i2)
    #print(xs)
    if not os.path.isfile(i1):
        print("对比源图片不能为空")
        return False,0,0
    if not os.path.isfile(i2):
        print("对比图片不能为空")
        return False,0,0
    try:
        img = cv2. imread(i1, 0)
        rw, rh = img. shape[:: - 1]
        img2 = img. copy()
        template = cv2. imread(i2, 0)
        w, h = template. shape[:: - 1]
        w0=0
        h0=0
        w1=0
        h1=0
        loc=(0,0)
        xsd=0.7
        if len(xs)==0:
            xsd = 0.7
        else:
            xsd,=xs
            
        #print(xsd)
        # All the 6 methods for comparison in a list
        methods = [ 'cv2.TM_CCOEFF' , 'cv2.TM_CCOEFF_NORMED' , 'cv2.TM_CCORR' ,
        'cv2.TM_CCORR_NORMED' , 'cv2.TM_SQDIFF' , 'cv2.TM_SQDIFF_NORMED' ]
        methods = [ 'cv2.TM_CCOEFF_NORMED' , 'cv2.TM_SQDIFF_NORMED' ]
        for meth in methods:
            img = img2. copy()
            #exec 语句用来执行储存在字符串或文件中的 Python 语句。
            # 例如，我们可以在运行时生成一个包含 Python 代码的字符串，然后使用 exec 语句执行这些语句
            #eval 语句用来计算存储在字符串中的有效 Python 表达式
            method = eval(meth)
            # Apply template Matching
            res = cv2. matchTemplate(img,template,method)
            
            #print("res"+str(res))
            min_val, max_val, min_loc, max_loc = cv2. minMaxLoc(res)
            '''
            print(min_val)
            print(max_val)
            print(min_loc)
            print(max_loc)
            '''
            if meth=="cv2.TM_CCOEFF_NORMED":        
                result_c=max_val
            if meth=="cv2.TM_SQDIFF_NORMED":
                (w0,h0)=min_loc
                result_s=1-min_val
            #print("相似度1 "+str(result_c))
            #print("相似度2 "+str(result_s))
            
        loc=(w0+w/2,h0+h/2)
        if rw<rh:
            #print("竖屏")
            #w1=(w0+w/2)*1080/rw
            #h1=(h0+h/2)*1920/rh
            w1=(w0+w/2)/2
            h1=(h0+h/2)/2
        else:
            #print("横屏")
            w1=(w0+w/2)/2
            h1=(h0+h/2)/2
            
        #print(loc)
        #cv2. destroyAllWindows()
        if result_c>xsd:
            return True,w1,h1
        else:
            print(result_c)
            return False,result_c,0
    except(Exception) as e:
        print(str(e))
        return False,0,0
    
