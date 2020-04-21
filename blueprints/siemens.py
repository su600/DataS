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
from struct import pack, unpack_from  # Pylogix 结构体解析
from blueprints.login import is_login
import blueprints.influxdb
# from blueprints.influxdb import influxDB #不能用from 要用import

siemens_ = Blueprint("siemens_",__name__)

'''
西门子库文件 python-snap7
'''
# import s7read
import snap7.client as client
from snap7.util import *
from snap7.snap7types import *


###################### 西门子 #######################################

@siemens_.route("/siemens",methods=("GET","POST"))
@is_login
def siemens():
    ## 反馈系统运行状态
    def s7connect(ip, rack, slot):
        try:
            plc = client.Client()
            # print(ip,rack,slot)
            plc.connect(ip, rack, slot)
        except Exception as e:
            flash("连接失败，请确认IP或网络连通性", "connect0")
        else:
            state = plc.get_cpu_state()
            flash(ip + " 连接成功", "connect1")
            return plc

    def s7disconnect():
        try:
            # plc = client.Client()
            # plc = client.Client()
            plc.disconnect()
        except Exception:
            flash("断开失败", "connect0")  ##connect0 失败提醒
        else:
            flash("已断开连接", "connect1")  ## connect1 操作成功提示

    def s7read(plc, iqm, address):

        ss = ""  # 标识I/Q/M
        t = areas[iqm]
        variable = []
        data = []
        # print(address)
        if address == '':
            address2 = 0.0
        else:
            address2 = (float(address))
        if t == 129:
            ss = "I "
        if t == 130:
            ss = "Q "
        if t == 131:
            ss = "M "

        b = (int(address2))
        c = (int((address2 - b) * 10))

        # print(t,b,c)
        try:
            variable.append(ss + address)
            # print(variable)
            # timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            result = plc.read_area(t, 0, b, 8)  ## 变量类型，0，地址起始，固定8位
            data.append(get_bool(result, 0, c))  ## 地址偏移值
            tt0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        except Exception as e:
            print(e)
        else:
            siemensdata0 = dict(zip(variable, data))
            # print(siemens0)
            return siemensdata0,tt0
    
    if request.method =="POST":
        # flash("run", "run")
        # print("222222222")
        forminfo = request.form.to_dict()
        # print(forminfo)

        # 该页面的表单信息，只要submit都传到这里，其中包括plc的连接信息 ip[str] rack[int] slot[int]
        # 还包括变量地址信息以及influxdb配置信息，(通过字典长度区分各个表单) 已更新为以submit的value来区分提交按钮
        global plc
        if forminfo["Action"]=="file" : ####
            try:
                f = request.files.get('file') ## 获取文件
                print(f.filename)
                f.save('D:/' + secure_filename(f.filename))  ## C盘写入权限受限Permission denied
            except Exception as e:
                print(e)
                flash(e,"uploadstatus")
            else:
                ## 保存测试
                flash("变量表上传成功", "uploadstatus")
                # try:
                #     f.save('D:/' + secure_filename(f.filename))  ## C盘写入权限受限Permission denied
                # except Exception as e:
                #     flash(e, "uploadstatus")
                # else:
                #     flash("变量表上传成功","uploadstatus")

        if forminfo["Action"] == "s7connect": #PLC 连接信息
            print(forminfo)
            plc=s7connect(str(forminfo["ipaddress"]),int(forminfo["rack"]),int(forminfo["slot"])) #数据类型转换
            # ip=forminfo["ipaddress"]

        if forminfo["Action"] == "s7disconnect":  # PLC 连接信息
            # print(forminfo)
            # plc = s7connect(str(forminfo["ipaddress"]), int(forminfo["rack"]), int(forminfo["slot"]))  # 数据类型转换
            s7disconnect()

        if  forminfo["Action"] == "s7read": #变量地址
            # print(forminfo)
            siemensdata,ttt=s7read(plc,forminfo["iqm"],forminfo["address"])
            # print(data)
            return render_template("siemens.html",siemensdata=siemensdata,ttt=ttt)

        if forminfo["Action"] == "influxdb": # influxdb连接信息
            print(forminfo)
            influxdbip = forminfo["influxdb"]
            token = forminfo["token"]
            measurement = forminfo["measurement"]
            cycle=forminfo["cycle"]
            # Blueprints 调用
            blueprints.influxdb.influxDB(influxdbip,token,measurement,cycle)
        # flash(forminfo,"connect1")
        # return redirect("#")
        # return render_template("siemens.html")
    return render_template("siemens.html")
    # return render_template("rockwell.html")
