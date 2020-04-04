#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/4/4 9:41
# @Author : jingwei
# @Site : 
# @File : send_mail.py
# @Software: PyCharm

# !/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def do_send(user_mail, plain_text):
    my_sender = 'jingwei_shi1205@sina.com'  # 发件人邮箱账号
    my_pass = 'b256d5982f196ab0'  # 发件人邮箱密码
    my_user = 'jingwei.shi@foxmail.com'  # 收件人邮箱账号，我这边发送给自己
    try:
        msg = MIMEText("用户电子邮箱："+user_mail+"\n"+plain_text, 'plain', 'utf-8')
        msg['From'] = formataddr(["word killer", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["jingwei", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "Word就是我的-用户反馈"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.sina.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        return True
    except:
        return False
