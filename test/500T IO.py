from blueprints.influxdb import *
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
# import numpy as np
# from struct import pack, unpack_from  # Pylogix 结构体解析
# from blueprints.login import is_login
#
# import blueprints.influxdb
#
# import threading
# from pylogix import PLC

global rockwellip,rockwell_device_list,taglist
rockwellip=''
rockwelldata=()
rockwell_device_list=[]
ttt=''
taglist=[]

def rockwellread():    #'读取函数'
    # print("readlist")
    print(taglist)
    ### 分批读取函数 每次读取10个变量
    # def readten(tags_list):
    #     l = len(tags_list)  # 变量表长度，如果大于10 必须分批读取保证不报错
    #     x = l // 10  # 取整
    #     y = l % 10  # 取余数
    #     a = 0  # 每一组变量的上标
    #     val = []  # 初始化列表 每一组变量值
    #     for n in range(x):
    #         if n < x:
    #             val = val + comm.Read(tags_list[10 * a:10 * (a + 1)])
    #             a += 1
    #             n += 1
    #         if n == x and y != 0:
    #             val = val + comm.Read(tags_list[10 * a:10 * a + y])
    #     vall = val
    #     return vall

    # with PLC() as comm:
    tagname=[]
    tagvalue=[]
    #     comm.IPAddress=rockwellip
    #     aa=readten(taglist) #调用函数分批读取变量
    aa=taglist
    ttt=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(aa)
    for a in aa:
        tagname.append(a.TagName)
        # 对于 IO 特殊处理 转换为0000/0000/0000/0000形式 #
        # IO长度不一定 暂定按16个 且形式不确定 IO模块数据类型复杂
        # todo 原版程序 根据500T IO解析列表，分情况处理 主要是长度不同 变量名也不同
        ##############################
        # if a.TagName == "Local:1:I.Data" or a.TagName == "Local:1:O.Data" :
        #     if  a.Value < 0 :
        #         a.Value = 65536 + a.Value
        #     b = ('{:016b}'.format(a.Value))[::-1] #转二进制并 高位补零 IO逆序输出
        #     b=list(b)
        #     b.insert(4, '/')
        #     b.insert(9, '/')
        #     b.insert(14, '/')
        #     a.Value = ''.join(b)
        # tagvalue.append(a.Value)
        ##############################

        # todo 测试用 仅包含IO变量 （原版在上面）
        # if a.TagName == "Local:1:I.Data" or a.TagName == "Local:1:O.Data" :
        # todo 需要区分数字量还是模拟量 数字量格式化为二进制 模拟量不格式化
        # todo 位数不同处理不同 16位和32位有交集 不应该从数字大小判断位数长度 根据位数长度 选择对应的变换函数
        # todo 仅针对数字量

        ## 16位DIO变换函数
        def DIO16(a):
            if a.Value < 0:
                # print(a)
                a.Value = 32767 - a.Value
            b = ('{:016b}'.format(a.Value))[::-1] #转二进制并 高位补零 IO逆序输出
            b=list(b)
            b.insert(4, '/')
            b.insert(9, '/')
            b.insert(14, '/')
            a.Value = ''.join(b)
            return a.Value

        ## 32位DIO变换函数
        def DIO32(a):
            if a.Value < 0:
                a.Value = 2147483647 - a.Value
            b = ('{:032b}'.format(a.Value))[::-1]  # 转二进制并 高位补零 IO逆序输出
            b = list(b)
            b.insert(4, '/')
            b.insert(9, '/')
            b.insert(14, '/')
            b.insert(19, '/')
            b.insert(24, '/')
            b.insert(29, '/')
            b.insert(34, '/')
            a.Value = ''.join(b)
            return a.Value

        # # todo 根据iotype进行转换 变量表中也需要判断解析 生成相应的表变量名
        # if IOtype是16位
        #     a.Value=DIO16(a)
        # if IOtype是32位
        #     a.Value=DIO32()
        # if IOtype是AIO
        #     不用转二进制

        tagvalue.append(a.Value)

        ######################################
        # todo 仅针对IO变量 读取不做格式化 模拟量用不用取正值？
        # tagvalue.append(a.Value)
        ######################################3

    # 输出到前端页面
    rockwelldata=dict(zip(tagname,tagvalue))
    # return rockwelldata
    print(rockwelldata)
    # return redirect("#data")
    # global influxdata
    # influxdata=rockwelldata
    # return render_template("rockwell.html",rockwelldata=rockwelldata,ttt=ttt),rockwelldata

def rockwellreadexcel():
    # print("readexcel"+file.filename)
    file="D:\IO原始列表.xlsx"
    # data = pd.DataFrame(pd.read_excel(file))
    # data2 = pd.read_excel(file, usecols=[0], header=None)  ##第一列 无表头 输出为DataFrame格式 带索引
    data2 = pd.read_excel(file)  ##输出为DataFrame格式 后续剔除未知类型

    data2=data2.dropna() ##剔除异常的nan

    # 变量筛选 不算是完全通用的筛选方式
    # isin()删选非IO变量  data2['TagType'].isin(["INT","DINT","BOOL", "REAL"]) 变量筛选
    data2 = data2[data2['TagType'].isin(["INT","DINT","BOOL", "REAL"])
                  | data2['TagName'].str.contains("Local:")
                  & ~data2['TagName'].str.contains(":C")
                  & ~data2['TagType'].str.contains("ASCII|MODULE") ]
    # print(data2)
    ## ["INT","DINT","BOOL",  "REAL","AB:Embedded_DiscreteIO:O:0","AB:Embedded_DiscreteIO:I:0"] "COUNTER","TIMER","DWORD"
    ##剔除程序名,C变量 和已知类型之外的数据，保留IO变量
    # data2 = data2['TagName']
    # print(data2)

    # 添加IO变量.Data
    # todo 变量表中需要判断解析 生成相应的表变量名
    # todo 存在重复筛选的问题 应该可以简化为一次
    # 筛选变量 根据IO性质，剔除无用OI变量 （I的剔除O O的剔除I）
    # 也可以写为 data2.TagType 不过看起来不够明显，修改不方便
    data2 = data2[(data2['TagType'].str.contains("IF")   & ~data2['TagType'].str.contains("O"))
                  | (data2['TagType'].str.contains("OF") & ~data2['TagType'].str.contains("I"))
                  | (data2['TagType'].str.contains("DI") & ~data2['TagType'].str.contains("O"))
                  | (data2['TagType'].str.contains("DO") & ~data2['TagType'].str.contains("I"))
                  | (data2['TagType'].str.contains("IT") & ~data2['TagType'].str.contains("O"))]
    # print(list(range(data2.shape[0])))
    # print(data2)
    data2=data2.reset_index(drop=True)  # todo 实际数据列表的数据删除了 但是索引依然存在 需要重新生成索引
    # print(data2)
    # todo 添加一列作为IOType 以下所有操作根据IOType进行 减少匹配和筛选 ======

    # todo 函数复用
    import re #正则表达式
    ccc=re.findall(r'_(.+?):', str(data2[data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O")]['TagType']))
    ccc=re.findall(r'\d+',str(ccc))
    print(ccc,type(ccc))
    # data2[data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O")]
    # (data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O"))
    # print(data2.shape[0])
    IF=data2.loc[data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O")]['TagName']
    # data2.loc[data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O")] = [IF.loc[0]['TagName'] + '.Ch' + '0' + 'Data',IF.loc[0]['TagType']]
    print(IF,type(IF))
    print(IF[0])

    # todo IF的大小和ccc的大小是一样的

    # todo 在嵌套循环里会多次循环 结果不对
    for i in range(int(ccc[0]) - 1):
        # print(i)
        if i == 0:
            data2.loc[data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O"), 'TagName'] += '.Ch' + str(i) + 'Data'

    # todo 两个一样的模块 需要分别对应处理  已实现 嵌套循环 添加.ChXData
    for n in range(len(ccc)):
        for i in range(int(ccc[0])-1):
            # print(i)
            # if i==0:
            #     data2.loc[data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O"), 'TagName'] += '.Ch' + str(i) + 'Data'
            data2.loc[data2.shape[0]+n*(int(ccc[0])-1)] = [IF[n]+'.Ch' + str(i+1) + 'Data','BOOL']
                # [data2.loc[data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O")]['TagName'] + '.Ch' + str(i+1) + 'Data'
                # ,data2[data2.TagType.str.contains("IF") & ~data2.TagType.str.contains("O")]['TagType']]

    print(data2)

    i=str(5)
    data2.loc[data2.TagType.str.contains("OF") & ~data2.TagType.str.contains("I"), 'TagName'] += '.Ch' + i + 'Data'
    data2.loc[data2.TagType.str.contains("DI") & ~data2.TagType.str.contains("O"), 'TagName'] += '.Data'
    data2.loc[data2.TagType.str.contains("DO") & ~data2.TagType.str.contains("I"), 'TagName'] += '.Data'
    data2.loc[data2.TagType.str.contains("IT") & ~data2.TagType.str.contains("O"), 'TagName'] += '.Ch' + i + 'Data'

    # print(data2)
    # print(data2,type(data2))
    global taglist
    taglist = data2.to_numpy().tolist()  # 转数组 转列表
    # taglist = sum(data2, [])  # 嵌套列表平铺 变量表list
    # print(taglist)

rockwellreadexcel()