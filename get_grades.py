#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/7/16 14:17
# @Author: https://github.com/ithou


'''
功能：模拟登陆教务系统，并实时爬取教务系统上的成绩信息，并在当前文件目录生csv格式Excel表
'''

import sys
import requests
from bs4 import BeautifulSoup
import csv

############# Linux 编码处理 #############
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://newjw.cduestc.cn/loginAction.do'  # 教务系统登录链接
data = {
    "zjh": "xxx",    # 学号
    "mm": "xxx"    # 密码
}
headers = {
   'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; '
                 'WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.'
                 '50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'
}

s = requests.Session()  # 创建session对象

r = s.post(url, data=data, headers=headers)  # 登录

########## 全部及格成绩页面 ##########
grades_link = "http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=" \
                   "2017-2018%D1%A7%C4%EA%B4%BA(%C1%BD%D1%A7%C6%DA)#2017-2018%E5%AD%A6%E5%B9%B" \
                   "4%E6%98%A5(%E4%B8%A4%E5%AD%A6%E6%9C%9F)"
r2 = s.post(grades_link, headers=headers)

soup = BeautifulSoup(r2.text, 'html.parser')
grades_list = soup.find_all('td', align="center")
table_title = ['课程号', '课序号', '课程名', '英文课程名', '学分', '课程属性', '成绩']

############## 标题 ##############
with open(r'/root/python/grades.csv', 'w+') as f:
    w = csv.writer(f)
    w.writerow(table_title)

############## 成绩 ##############
cnt = 0  # 计数
for i in range(len(grades_list)):
    with open(r'/root/python/grades.csv', 'a+') as f:
        f.write(grades_list[i].text.strip()+','+'\t')
        cnt = cnt + 1
        if cnt == 7:
            f.write("\n")
            cnt = 0
        f.close()
print("Okay!")