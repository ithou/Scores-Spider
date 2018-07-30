#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/7/22 17:46
# @Author: https://github.com/ithou

import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header

from_addr = "xxx@xx.xx"  # 发件人邮箱地址
to_addr = "yyy@yy.yy"  # 收件人邮箱地址
password = "***"  # 账号POP3/SMTP登录授权码
smtp_server = "smtp.xx.xx"  # smtp服务器

# 邮件对象
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = Header("叮！您的成绩更新啦！", "utf-8").encode()

# 邮件文字内容
msg.attach(MIMEText("您的成绩又更新啦！下载附件查看。 <br/> ——Send automatically by Python-Spider.", "html", "utf-8"))

# 添加附件，从本地读取一个文件
part = MIMEBase('application', 'octet-stream')
part.set_payload(open(r'/root/python/grades.csv', 'rb').read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename='grades.csv')
msg.attach(part)

server = smtplib.SMTP_SSL(smtp_server, 465)  # 默认端口25，用SSL 465端口，以防在Linux上出现异常
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()