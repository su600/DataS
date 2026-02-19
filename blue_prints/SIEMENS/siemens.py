from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file,Blueprint
from flask_bootstrap import Bootstrap

import random, datetime
from functools import wraps
import time
import functools
import os

from snap7.client import Client
from werkzeug.utils import secure_filename
import csv
import pandas as pd
import numpy as np
from struct import pack, unpack_from  # Pylogix 结构体解析
from blue_prints.LOGIN.login import is_login
from blue_prints.INFLUXDB.influxdb import influxDB
# from blueprints.influxdb import influxDB #不能用from 要用import

siemens_ = Blueprint("siemens_",__name__)

'''
西门子库文件 python-snap7
'''
import snap7.client as client
from snap7.util import *
from snap7.snap7types import *
import ctypes
import struct
from snap7.common import check_error
# from snap7.snap7types import S7DataItem, S7AreaDB, S7WLByte
from snap7.snap7types import *
from snap7 import util

global tag_name,tag_type, tag_address,data_type,plc
tag_name=[]

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
            plc.disconnect()
            plc.destroy()
        except Exception:
            flash("断开失败", "connect0")  ##connect0 失败提醒
        else:
            flash("已断开连接", "connect1")  ## connect1 操作成功提示

    # todo 仅支持BOOL，暂未添加其它数据类型
    def s7read(plc, iqm, address):
        '''
        单个地址变量读取
        '''
        ss = ""  # 标识I/Q/M
        t = areas[iqm]
        variable = []
        data = []
        print(address)
        if address == '':
            address2 = "0.0"
        else:
            address2 = (str(address))
        if t == 129:
            ss = "I "
        if t == 130:
            ss = "Q "
        if t == 131:
            ss = "M "

        b = int(address2.split(".")[0])
        c = int(address2.split(".")[1])
        # 字符串解析 以"."分割
        # 注意  强制类型转换精度不一致 （address2 - b） * 10 导致0.99999取整变0


        print(t,b,c)
        try:
            variable.append(ss + address)
            # print(variable)
            # timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            result = plc.read_area(t, 0, b, 8)  ## 变量类型，0，地址起始，固定8位
            data.append(get_bool(result, 0, c))  ## 地址偏移值
            print(get_bool(result, 0, c))
            tt0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        except Exception as e:
            print(e)
        else:
            # print(data)
            siemensdata0 = dict(zip(variable, data))
            # print(siemens0)
            return siemensdata0,tt0

    def s7_read_excel(file):
        '''
          上传变量表后调用 即开始读取excel 生成待读取的变量表
       '''
        data2 = pd.read_excel(file)  ##输出为DataFrame格式 后续剔除未知类型
        # data2 = data2.dropna()  ##剔除异常的nan

        # 变量表筛选 变量类型转换
        data2 = data2[['Name', 'Data Type', 'Logical Address']]
        data2['Logical Address'] = data2['Logical Address'].str.replace('%', '').str.replace('I', 'PE') \
            .str.replace('Q', 'PA').str.replace('M', 'MK')

        # 例如 AA I1.0 Bool
        tag_name = data2['Name'].to_numpy().tolist() # AA
        tag_type = data2['Logical Address'].str[:2].to_numpy().tolist()  # 类型 I
        tag_address = data2['Logical Address'].str[2:].to_numpy().tolist()  # 地址 1.0
        data_type = data2['Data Type'].to_numpy().tolist() # 数据类型
        return tag_name,tag_type,tag_address,data_type

    def s7_multi_read(plc, tag_type, tag_address, data_type, tag_name):
        '''
            从s7_read_excel处理完的变量表中批量读取变量
        '''
        taglens = len(tag_type)
        data_items = (S7DataItem * taglens)()  # 括号 数组

        # fixme 如果只有一个变量的情况 可能会有bug
        # 生成 data_items 待读取的变量结构体
        for i in range(taglens):
            # print(i)
            data_items[i].Area = areas[tag_type[i]]  # 数据类型
            data_items[i].WordLen = ctypes.c_int32(S7WLByte)
            data_items[i].Result = ctypes.c_int32(0)
            data_items[i].DBNumber = ctypes.c_int32(0)  # DB块 非DB写0
            data_items[i].Start = ctypes.c_int32(int(tag_address[i].split('.')[0]))  # byte地址
            data_items[i].Amount = ctypes.c_int32(8)  # 读取8位

        for di in data_items:
            # create the buffer
            buffer = ctypes.create_string_buffer(di.Amount)
            # cast the pointer to the buffer to the required type
            pBuffer = ctypes.cast(ctypes.pointer(buffer),ctypes.POINTER(ctypes.c_uint8))
            di.pData = pBuffer

        # snap7 read_multi_vars has a limitation of ~20 variables per call
        # When reading more than 20 variables, split into batches
        BATCH_SIZE = 20
        taglens = len(data_items)
        
        if taglens <= BATCH_SIZE:
            # Read all at once if 20 or fewer variables
            result, data_items = plc.read_multi_vars(data_items)
        else:
            # Read in batches for more than 20 variables
            num_batches = (taglens + BATCH_SIZE - 1) // BATCH_SIZE  # Ceiling division
            
            for batch_num in range(num_batches):
                start_idx = batch_num * BATCH_SIZE
                end_idx = min(start_idx + BATCH_SIZE, taglens)
                
                # Create batch array
                batch_items = (S7DataItem * (end_idx - start_idx))()
                for i in range(end_idx - start_idx):
                    batch_items[i] = data_items[start_idx + i]
                
                # Read this batch
                result, batch_results = plc.read_multi_vars(batch_items)
                if result != 0:
                    # If batch read fails, raise an error
                    raise Exception(f"Batch {batch_num + 1} read failed with error code: {result}")
                
                # Copy results back to original data_items
                for i in range(end_idx - start_idx):
                    data_items[start_idx + i] = batch_results[i]
        # print('读取的原始数据',data_items)
        ttt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        for di in data_items:
            check_error(di.Result)

        result_values = []
        # function to cast bytes to match data_types[] above
        # byte_to_value = [util.get_bool, util.get_real, util.get_int,util.get_dword,util.get_string]
        # unpack and test the result of each read
        # todo 做一个函数列表，合并循环。逻辑上需要先读取，后get_bool
        for i in range(0, len(data_items)):

            ddd = data_items[i]
            d_bit = int(tag_address[i].split('.')[1])
            if data_type[i] == 'Bool':
                value = util.get_bool(ddd.pData, 0, d_bit)
            elif data_type[i] == 'Real':
                value = util.get_real(ddd.pData, d_bit)
            elif data_type[i] == 'Int':
                value = util.get_int(ddd.pData, d_bit)
            elif data_type[i] == 'Dword':
                value = util.get_dword(ddd.pData, d_bit)
            elif data_type[i] == 'String':
                value = util.get_string(ddd.pData, d_bit)
            result_values.append(value)

        # fixme
        # client.disconnect()
        # client.destroy()

        siemensdata = dict(zip(tag_name, result_values))
        # print(siemensdata)
        return siemensdata, ttt

    # global plc
    # global tag_type, tag_address

    if request.method =="POST":
        forminfo = request.form.to_dict()

        # 该页面的表单信息，只要submit都传到这里，其中包括plc的连接信息 ip[str] rack[int] slot[int]
        # 还包括变量地址信息以及influxdb配置信息，(通过字典长度区分各个表单) 已更新为以submit的value来区分提交按钮

        if forminfo["Action"]=="file" : ####
            try:
                file = request.files.get('file')
                # print(file.filename)
                # todo 保存目录 默认改为当前目录下的Excel文件夹内
                file.save('D:/' + secure_filename(file.filename))  ## C盘写入权限受限Permission denied 暂存在D盘，linux中应该没问题
                global tag_name,tag_type,tag_address,data_type
                tag_name,tag_type,tag_address,data_type=s7_read_excel(file) # 上传变量表后即开始读取excel 生成变量表
            except Exception as e:
                # print(e)
                flash(e,"uploadstatus")
                # new_name=(secure_filename(file.filename)).split('.',[0])+'_1'+(secure_filename(file.filename)).split('.',[1])
                # print(new_name)
                # file.save('D:/' + secure_filename(new_name))
            else:
                flash("变量表上传成功", "uploadstatus")


        if forminfo["Action"] == "s7connect": #PLC 连接信息
            # print(forminfo)
            global plc
            print(str(forminfo))
            plc=s7connect(str(forminfo["ipaddress"]),int(forminfo["rack"]),int(forminfo["slot"])) #数据类型转换
            # ip=forminfo["ipaddress"]

        if forminfo["Action"] == "s7disconnect":  # PLC 连接信息
            s7disconnect()

        if  forminfo["Action"] == "s7read": #变量地址

            siemensdata,ttt=s7read(plc,forminfo["iqm"],forminfo["address"])
            return render_template("siemens.html",siemensdata=siemensdata,ttt=ttt)

        if  forminfo["Action"] == "s7multiread": #变量地址
            try:
                siemensdata,ttt=s7_multi_read(plc, tag_type, tag_address,data_type,tag_name)
            except Exception as e:
                flash(e,'uploadstatus')
                # redirect('#')
            else:
                return render_template("siemens.html",siemensdata=siemensdata,ttt=ttt)

        if forminfo["Action"] == "influxdb": # influxdb连接信息
            influxdbip = forminfo["influxdb"]
            token = forminfo["token"]
            measurement = forminfo["measurement"]
            cycle=forminfo["cycle"]
            # Blueprints 调用 已import
            influxDB(influxdbip,token,measurement,cycle)
        # flash(forminfo,"connect1")
        # return redirect("#")
        # return render_template("siemens.html")
    return render_template("siemens.html")

