from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file,Blueprint
from flask_bootstrap import Bootstrap

import random, datetime
from functools import wraps
import time
import functools
import os
from werkzeug.utils import secure_filename
import csv
import pandas as pd
import numpy as np
from struct import pack, unpack_from

import socket # 与机器人上位机软件 socket 通信

import asyncio

from blue_prints.LOGIN.login import is_login 

kuka_ = Blueprint("kuka",__name__)

'''
库卡机器人
socket通信
Socket 方式连接
IP:192.6.94.10
PORT:6008
发送1-6，分别返回制孔机器人位姿、制孔机器人关节角度、铆接机器人位姿、铆接机器人关节角度、末端数据、相机数据。
'''


########################### KUKA机器人 ################################
@kuka_.route("/kuka",methods=["POST","GET"])
@is_login
def kuka():
    # return render_template("b.html")

    def kuka_connect(ip,port):
        '''
        与KUAK机器人QYB上位机程序socket通信
        :param ip: ip地址 192.168.1.10
        :param port: socket端口 6008
        :return: 机器人、末端、相机状态信息
        '''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
        except socket.error as e:
            print(e)
            # sys.exit(1)
        else:
            # print(s.recv(1024))  # 目的在于接受：Accept new connection from (...
            # data = input('请输入发送命令: ').strip().encode()
            data = '1'.strip().encode()
            while 1:
                s.send(data)
                rec = s.recv(1024).decode()
                print('接收信息', rec)
                time.sleep(0.1) # 100ms周期请求数据
                # print(aaa.decode('gbk'))
            s.close()

    if request.method=='POST':
        forminfo=request.form.to_dict() ## to_dict()加括号

        if forminfo['Action']=='connect':
            ipaddress=forminfo['ipaddress']
            port=int(forminfo['port'])
            kuka_connect(ipaddress,port)
            flash(f'机器人{ipaddress}连接成功 开始读取数据',"connect1")
            # return render_template("kuka.html")
    return render_template("kuka.html")