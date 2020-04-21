# from blueprints.influxdb import *
# from main import *
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file,Blueprint,current_app
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

import threading

from flask import copy_current_request_context
import gevent

rockwell_ = Blueprint("rockwell_",__name__)

'''
罗克韦尔AB Pylogix 0.6.2
'''
# from pylogix import *
from pylogix import PLC

class Timer(object):

    def __init__(self, data):
        self.PRE = unpack_from('<i', data, 6)[0]
        self.ACC = unpack_from('<i', data, 10)[0]
        bits = unpack_from('<i', data, 2)[0]
        self.EN = get_bit(bits, 31)
        self.TT = get_bit(bits, 30)
        self.DN = get_bit(bits, 29)

class Motion(object): # Su 仿照Timer类型添加Motion类型 ToDo

    def __init__(self, data):
        self.PRE = unpack_from('<i', data, 6)[0]
        self.ACC = unpack_from('<i', data, 10)[0]
        bits = unpack_from('<i', data, 2)[0]
        self.EN = get_bit(bits, 31)
        self.TT = get_bit(bits, 30)
        self.DN = get_bit(bits, 29)

def get_bit(value, bit_number):
    '''
    Returns the specific bit of a word
    '''
    mask = 1 << bit_number
    if (value & mask):
        return True
    else:
        return False


######################### 罗克韦尔 ##############################

global rockwellip,rockwell_device_list,taglist
rockwellip=''
rockwelldata=()
rockwell_device_list=[]
ttt=''
taglist=[]

@rockwell_.route("/rockwell",methods=["POST","GET"])
@is_login
def rockwell():
    ## Rockwell AB PLC # #108厂房设备
    return render_template("rockwell.html")

@rockwell_.route("/rockwellread",methods=["POST","GET"])
@is_login
def rockwellread():    #'读取函数'
    # print("readlist")
    print(taglist)
    ### 分批读取函数 每次读取10个变量
    def readten(tags_list):
        l = len(tags_list)  # 变量表长度，如果大于10 必须分批读取保证不报错
        x = l // 10  # 取整
        y = l % 10  # 取余数
        a = 0  # 每一组变量的上标
        val = []  # 初始化列表 每一组变量值
        for n in range(x):
            if n < x:
                val = val + comm.Read(tags_list[10 * a:10 * (a + 1)])
                a += 1
                n += 1
            if n == x and y != 0:
                val = val + comm.Read(tags_list[10 * a:10 * a + y])
        vall = val
        return vall

    with PLC() as comm:
        tagname=[]
        tagvalue=[]
        comm.IPAddress=rockwellip
        aa=readten(taglist) #调用函数分批读取变量
        ttt=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(aa)
        for a in aa:
            tagname.append(a.TagName)
            # 对于 IO 特殊处理 转换为0000/0000/0000/0000形式 #
            # todo IO长度不一定 暂定按16个 且形式不确定 IO模块数据类型复杂 考虑先不读取
            if a.TagName == "Local:1:I.Data" or a.TagName == "Local:1:O.Data" :
                if a.Value < 0:
                    a.Value = 65536 + a.Value
                b = ('{:016b}'.format(a.Value))[::-1] #转二进制并 高位补零 IO逆序输出
                b=list(b)
                b.insert(4, '/')
                b.insert(9, '/')
                b.insert(14, '/')
                a.Value = ''.join(b)
            tagvalue.append(a.Value)
        # 输出到前端页面
        rockwelldata=dict(zip(tagname,tagvalue))
        # return rockwelldata
        # print(rockwelldata)
        # return redirect("#data")
        # global influxdata
        # influxdata=rockwelldata
    return render_template("rockwell.html",rockwelldata=rockwelldata,ttt=ttt),rockwelldata

def rockwellreadexcel(file):
    print("readexcel"+file.filename)
    # data = pd.DataFrame(pd.read_excel(file))
    # data2 = pd.read_excel(file, usecols=[0], header=None)  ##第一列 无表头 输出为DataFrame格式 带索引
    data2 = pd.read_excel(file)  ##输出为DataFrame格式 后续剔除未知类型
    # data2=data2.dropna() ##剔除异常的nan
    data2 = data2[data2['TagType'].isin(["INT","DINT","BOOL", "REAL"]) | data2['TagName'].str.contains("Local:") & ~data2['TagName'].str.contains(":C")  ]
    ## ["INT","DINT","BOOL",  "REAL","AB:Embedded_DiscreteIO:O:0","AB:Embedded_DiscreteIO:I:0"] "COUNTER","TIMER","DWORD"
    ##剔除程序名,C变量 和已知类型之外的数据，保留IO变量
    data2 = data2['TagName']
    # print(data2)

    # 添加IO变量.Data
    data2[data2.str.contains("Local:")] = data2[data2.str.contains("Local:")] + ".Data"

    print(data2)
    global taglist
    taglist = data2.to_numpy().tolist()  # 转数组 转列表
    # taglist = sum(data2, [])  # 嵌套列表平铺 变量表list
    print(taglist)

@rockwell_.route("/rockwells",methods=["POST","GET"])
@is_login
def rockwells():
    with PLC() as comm:
        # 设备扫描
        deviceip = []
        devicename = []
        devices = comm.Discover()
        for device in devices.Value:
            deviceip.append(device.IPAddress)
            devicename.append(device.ProductName + ' ' + device.IPAddress)
        global rockwell_device_list
        rockwell_device_list = dict(zip(devicename, deviceip))  # 创建设备字典 写入全局变量
        scanresult="扫描到"+str(len(rockwell_device_list))+"台设备"
        print(scanresult)
        flash(scanresult,"scanresult") #扫描完成flash提示
        return redirect("rockwellscan")
        # dev_list=str(device_dict)
        # return redirect(url_for(rockwell)) # url_for函数跳转
        # flash(device_dict,"device_dict") #设备扫描结果显示到前端页面下拉列表

# 考虑开始连接会再次扫描设备，因此将s和scan分开 s扫描 之后跳转scan进行选择和表单操作 url为/rockwellscan
@rockwell_.route("/rockwellscan",methods=["POST","GET"])
@is_login
def rockwellscan():
        if request.method == "POST":
            flash("run", "run")
            forminfo=request.form.to_dict() ## to_dict()加括号
            # 该页面的表单信息，只要submit都传到这里
            # forminfo=request.form.get('devicelist') # 获取到的value是str字符串
            # 还包括变量地址信息以及influxdb配置信息，通过字典长度区分各个表单
            # 已更新为 根据action value区分表单
            # print(forminfo)
            # print(type(forminfo))
            # aa=type(forminfo)

            ######## 每次“开始连接”实际只是获取选择的设备ip并写入全局变量
            # 程序逻辑调整为rockwellscan运行后跳转rockwellscan2 但是页面会整体刷新造成列表变化~~~~~~~~~~~
            if forminfo["Action"]=="rockwellip" : # AB PLC 连接信息 只需要IP
                print(forminfo)
                aa=(forminfo["devicelist"]).split(" ")
                aa=aa[len(aa)-1] #获取ip
                global rockwellip # 全局变量 要先声明globa 再修改
                rockwellip=aa
                ss=("已连接到 "+str(forminfo["devicelist"]))
                flash(ss, "scanresult")  # 连接完成
                # print(rockwellip)

            # if (forminfo)=={}:  # 上传变量表 #
            if forminfo["Action"]=="file" : #### 是excel就调用readexcel
                # print("22222222222")
                try:
                    file = request.files.get('file')
                    file.save('D:/' + secure_filename(file.filename))  ## C盘写入权限受限Permission denied 暂存在D盘，linux中应该没问题
                    rockwellreadexcel(file)
                except Exception as e:
                    # print(e)
                    flash(e, "uploadstatus")
                else:
                    # 保存测试
                    flash("变量表上传成功", "uploadstatus")

            # if len(forminfo) == 2:  # 变量地址
            #     print(forminfo)
            #     data = s7read(plc, forminfo["iqm"], forminfo["address"])
            #     print(data)
            #     # return data
            if forminfo["Action"]=="influxdb":  # influxdb连接信息
                print(forminfo)
                influxdbip = forminfo["influxdb"]
                token = forminfo["token"]
                measurement = forminfo["measurement"]
                cycle = forminfo["cycle"]
                flash("写入InfluxDB", "influx")

                # 添加线程 todo 上下文处理/线程的外部停止
                # from flask import current_app
                # from main import app
                # app_ctx = app.app_context()
                # app_ctx.push()
                # with app.test_request_context("/rockwellscan"):
                #     print(current_app.name)
                    # influxdbip = forminfo["influxdb"]
                    # token = forminfo["token"]
                    # measurement = forminfo["measurement"]
                    # cycle = forminfo["cycle"]
                # print(current_app)
                # app.app_context().push()

                t1 = threading.Thread(target= blueprints.influxdb.influxDB, args=(influxdbip, token, measurement, cycle,))
                # t1.setDaemon(True)
                t1.start()
                # app_ctx.pop()
                # influxDB(influxdbip, token, measurement, cycle)

        # return redirect("#")
        # flash(rockwell_device_list,"dev_list") #flash只能传递字符串
        # return jsonify()
        # return redirect(url_for("rockwell"))
        return render_template("rockwell.html",dev_list=rockwell_device_list)#设备扫描结果显示到前端页面下拉列表
    ## 定向页面逻辑，此处要在rockwellscan中处理POST请求
    ## 前端调用后台程序 href=“xx” 通过路由调用，还有没有别的方法 采用url_for()跳转 参考登录函数处理方法
    # return redirect("#")

@rockwell_.route("/rockwell_get_all_vars")
@is_login
#### 获取所有变量 并下载 # 待办，剔除程序名称，编写变量读取函数，连续获取变量表 时间不变bug
def rockwell_get_all_vars(): #
    # print("111111111111111")
    with PLC() as comm:
        # print("111111111111")
        ####### 无法连续运行重复获取变量表？ 连续点击不进入循环 直接下载附件？？ 如果要刷新变量表需要再次“开始连接”##############
        print(rockwellip)
        if rockwellip=='':
            print("请先选择设备IP地址")
        else:
            print(rockwellip)
            comm.IPAddress = rockwellip #全局变量
            # comm.IPAddress="192.168.100.200"
            # print("2222222222")
            try:
                tags = comm.GetTagList() #输出是Response结构体类型需要解析
                comm.Close()
            except Exception as e:
                print(e)
                #缺一个return ，读取错误的错误处理
            else:
                tagname=[]
                tagtype=[]
                head=["TagName","TagType"]
                for t in tags.Value:
                    tagname.append(t.TagName)
                    tagtype.append(t.DataType)
                taglist = pd.DataFrame({'tagname': tagname, 'tagtype': tagtype}) #采用Pandas格式化
                # print(taglist)
                tt = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') #时间标识符
                filepath=("D:/Taglist "+tt+".xlsx")
                print(filepath)
                ## 变量表文件暂存以备发送和自动读取
                taglist.to_excel(filepath, encoding='utf-8', index=False, header=head) #写入excel
                ## 变量表文件下载
                return send_file(filepath,as_attachment=True) #向前端发送文件 下载 比send_from_directory简化
                # return send_from_directory(filepath,as_attachment=True) #