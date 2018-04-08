#!/usr/bin/env python
# coding=utf-8

import json
import urllib2
import httplib
import socket
import MySQLdb
import time
import subprocess
import os

server_url="http://www.easybots.cn/api/holiday.php?m=" #For day ?d
month="201801,201802,201803,201804,201805,201806,201807,201808,201809,201810,201811,201812"
curDate="20180501"
host='www.baidu.com'

def InsertData(TableName,dic,curDate):
    rtn='0'
    try:
        conn=MySQLdb.connect(host='localhost',user='fryduck',passwd='abc,123.',db='Test',port=3306,charset='utf8')  #链接数据库
        cur=conn.cursor()
        sql_create="CREATE TABLE IF NOT EXISTS %s(YM CHAR(10) NOT NULL, HOLIDAY CHAR(3) NOT NULL)" %TableName
        cur.execute(sql_create)
        #表存在，直接从表中根据当天日期查询是否节假日
        sql_select="SELECT * FROM %s WHERE YM = %s" %(TableName,curDate[0:6])
        cur.execute(sql_select)
        if len(cur.fetchall()) != 0:
            sql_select="SELECT * FROM %s WHERE YM = %s AND HOLIDAY = %s" %(TableName,curDate[0:6],curDate[-2:])
            cur.execute(sql_select)
            if len(cur.fetchall()) == 0:
                subprocess.call(["perl","/{HOME}/test.pl"])
            else:
                print "It is holiday"
        else:
        #表不存在，往空表中写入数据
            print "Insert Data"
            try:
                for each_items in dic:
                    for i in dic[each_items].keys():
                        cur.execute("INSERT INTO %s(YM,HOLIDAY) VALUES(%s,%s)" %(TableName,each_items,i))
                conn.commit()
            except:
                #写入数据失败时，回滚当前表
                conn.rollback()
                rtn='1'
    except MySQLdb.Error,e:
        print ("MySQLdb error %s:%s" %(e.args[0],e.args[1]))
        rtn='1'
    cur.close()
    conn.close()
    return rtn

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
    InsertData('Kq',vop_data,curDate)

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
