"""
Example ussage of the read_multi_vars function
This was tested against a S7-319 CPU
"""
import pandas as pd
import ctypes
import struct

import snap7
from snap7.common import check_error
# from snap7.snap7types import S7DataItem, S7AreaDB, S7WLByte
from snap7.snap7types import *
from snap7 import util
import time

client = snap7.client.Client()
client.connect('192.168.100.111', 0, 1)

# print('请输入变量 空格分隔')
# taglist=input()
# taglist=list(taglist)
# ######################### 分割：类型/byte/bit三个参数
# print(taglist)

# global plc
global tag_type, tag_address,data_type
plc=client

def s7_read_excel(file):
    '''
      上传变量表后调用 即开始读取excel 生成待读取的变量表
   '''
    # print("读取excel  ssss")

    data2 = pd.read_excel(file)  ##输出为DataFrame格式 后续剔除未知类型
    # data2 = data2.dropna()  ##剔除异常的nan

    data2 = data2[['Name', 'Data Type', 'Logical Address']]
    data2['Logical Address'] = data2['Logical Address'].str.replace('%', '').str.replace('I', 'PE') \
        .str.replace('Q', 'PA').str.replace('M', 'MK')
    # print(data2)
    # global tag_type, tag_address
    # areas = ADict({
    #     'PE': 0x81,I
    #     'PA': 0x82,Q
    #     'MK': 0x83,M
    #     'DB': 0x84,
    #     'CT': 0x1C,
    #     'TM': 0x1D,
    # })
    global tag_name,tag_type, tag_address, data_type
    # 例如 I1.0
    tag_name = data2['Name'].to_numpy().tolist()
    tag_type = data2['Logical Address'].str[:2].to_numpy().tolist()  # 类型 I 对应的areas字典key
    tag_address = data2['Logical Address'].str[2:].to_numpy().tolist()  # 地址 0.1
    data_type = data2['Data Type'].to_numpy().tolist()
    # return tag_type,tag_address
    # tag_address =list(map(float,tag_address))
    # print(tag_type)
    # print(tag_address)
    # print(data_type)


def s7_multi_read(plc, tag_type, tag_address,data_type,tag_name):
    '''
    从s7_read_excel处理完的变量表中批量读取变量
    '''
    # print('s7multiread函数')
    # print(tag_type, tag_address)
    taglens = len(tag_type)
    # print(taglens)
    # l = taglens  # 变量表长度，如果大于20 必须分批读取 snp7
    # x = (l // 20) +1  # 取整加1 组数
    # y = l % 20  # 取余数
    # dataitemsgroup=[]
    # for i in range(x):
    #     dataitemsgroup.append("data_items"+str(i))

    # for i in dataitemsgroup:
    #     if i < x:
    #         dataitemsgroup = (S7DataItem * pass)()
    #     data_items[i].Area = areas[tag_type[i]]  # 数据类型
    #     data_items[i].WordLen = ctypes.c_int32(S7WLByte)
    #     data_items[i].Result = ctypes.c_int32(0)
    #     data_items[i].DBNumber = ctypes.c_int32(0)  # DB块 非DB写0
    #     data_items[i].Start = ctypes.c_int32(int(tag_address[i].split('.')[0]))  # byte地址
    #     data_items[i].Amount = ctypes.c_int32(8)  # 读取8位
        #     val = val + plc.read_multi_vars(data_items[20 * a:20 * (a + 1)])
        #     a += 1
        #     n += 1
        # if n == x and y != 0:
        #     val = val + plc.read_multi_vars(data_items[20 * a:20 * a + y])
        #

    # a = 0  # 每一组变量的上标
    # val = []  # 初始化列表 每一组变量值
    # for n in range(x):
    #     if n < x:
    #         val = val + plc.read_multi_vars(data_items[20 * a:20 * (a + 1)])
    #         a += 1
    #         n += 1
    #     if n == x and y != 0:
    #         val = val + plc.read_multi_vars(data_items[20 * a:20 * a + y])
    # val2 = val
    # return val2
    data_items = (S7DataItem * taglens)()  # 括号 数组
    # print(type(data_items))
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

        # data_items[i].Bit = tag_address[i].split('.')[1] # 偏移量
    # print(type(data_items))
    # print(type(data_items[2]))
    # print(type(data_items[0:20]))
    # create buffers to receive the data
    # use the Amount attribute on each item to size the buffer
    for di in data_items:
        # create the buffer
        buffer = ctypes.create_string_buffer(di.Amount)

        # cast the pointer to the buffer to the required type
        pBuffer = ctypes.cast(ctypes.pointer(buffer),
                              ctypes.POINTER(ctypes.c_uint8))
        di.pData = pBuffer
        # di.Bit = di.Bit

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

    # for di in data_items:
    #     check_error(di.Result)

    result_values = []
    # function to cast bytes to match data_types[] above
    # byte_to_value = [util.get_bool, util.get_real, util.get_int,util.get_dword,util.get_string]
    # unpack and test the result of each read
    # todo 做一个函数列表，合并循环。逻辑上需要先读取，后get_bool
    for i in range(0, len(data_items)):
        # btv = byte_to_value[i]
        ddd = data_items[i]
        # print(ddd)
        d_bit = int(tag_address[i].split('.')[1])
        # value = btv(di.pData, 0)
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
        # assert isinstance(value, object)
        result_values.append(value)
    # print(result_values)

    # todo
    # client.disconnect()
    # client.destroy()

    siemensdata = dict(zip(tag_name, result_values))
    print(siemensdata)
    return siemensdata, ttt
    # return render_template("rockwell.html", siemensdata=siemensdata, ttt=ttt)


file='Z:PLC11111Tags.xlsx'
start=time.time()
s7_read_excel(file)
s7_multi_read(plc, tag_type, tag_address,data_type,tag_name)
end=time.time()
print(end-start)
client.disconnect()
client.destroy()