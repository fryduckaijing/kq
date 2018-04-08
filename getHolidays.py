#!/usr/bin/env python
# coding=utf-8

import json
import urllib2
import httplib
import socket
import MySQLdb
import time
import os

server_url="http://www.easybots.cn/api/holiday.php?m=" #For day ?d
month="201801,201802,201803,201804,201805,201806,201807,201808,201809,201810,201811,201812"
curDate="20180501"
host='www.baidu.com'

def InsertData(TableName,dic):
    conn=MySQLdb.connect(host='localhost',user='fryduck',passwd='abc,123.',db='Test',port=3306)  #链接数据库
    cur=conn.cursor()
    COLstr='' #列的字段
    ROWstr='' #行的字段

    for i,j in dic.items():
        ColumnStyle=' VARCHAR(20)'
        COLstr=COLstr+' '+i+ColumnStyle+','
        for key in dic[i].keys():
            ROWstr=(ROWstr+'"%s"'+',')%(key)

    #判断表是否存在，存在执行try，不存在执行except新建表，再Insert
    try:
        cur.execute("SELECT * FROM %s"%(TableName))
        cur.execute("INSERT INFO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
    except MySQLdb.Error,e:
        cur.execute("CREATE TABLE %s (%s)"%(TableName,COLstr[:-1]))
        cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
    conn.commit()
    cur.close()
    conn.close()

def Get_WebServerTime(host):
    try:
        conn=httplib.HTTPConnection(host,80,timeout=5)
        conn.request("GET","/")
        r=conn.getresponse()
    except (httplib.HTTPException,socket.timeout):
        time.localtime(time.time())
        return time.strftime('%Y%m%d',time.localtime(time.time()))
    else:
        ts=r.getheader('date') #获取所有的http头

        #将GMT时间转换成北京时间
        ltime=time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
        ttime=time.localtime(time.mktime(ltime)+8*60*60)
        caltime=time.strftime('%Y%m%d',ttime)
        return caltime

def IsHolidays(server_url,month,curDate):
    vop_url_request=urllib2.Request(server_url+month)
    vop_response=urllib2.urlopen(vop_url_request)

    vop_data=json.loads(vop_response.read())
    InsertData('Kq',vop_data)
    print(vop_data)

    _month=curDate[0:6]
    _date=curDate[-2:]
    if vop_data[_month].has_key(_date):
        return vop_data[_month][_date]
    else:
        return '0'

curDate=Get_WebServerTime(host)
isHolidays=IsHolidays(server_url,month,curDate)

if isHolidays=='0':
    print("this day is weekday")
elif isHolidays=='1':
    print('This day is weekend')
elif isHolidays=='2':
    print('This day is holiday')
else:
    print('Error')
