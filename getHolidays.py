#!/usr/bin/env python
# coding=utf-8

import json
import urllib2
#date = "20170530"
month = "201805,201806"
server_url = "http://www.easybots.cn/api/holiday.php?m=" #For day ?d

vop_url_request = urllib2.Request(server_url+month)
vop_response = urllib2.urlopen(vop_url_request)

vop_data= json.loads(vop_response.read())

print vop_data

if vop_data["201805"]["01"]=='0': #20180501
    print "this day is weekday"
elif vop_data["201805"]["01"]=='1':
    print 'This day is weekend'
elif vop_data["201805"]["01"]=='2':
    print 'This day is holiday'
else:
    print 'Error'
