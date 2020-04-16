'''
Pandas 测试程序
20200416 制作变量表 添加筛选IO变量并 添加后缀.Data
实际IO类型比较复杂 读取处理有难度 需每一种都针对性处理 位数/Byte/等都不一样 对应范围也不一样
'''
import pandas as pd
import numpy as np

file="D:\ABPLCdata0919第二次.xlsx"
data2 = pd.read_excel(file)  ##输出为DataFrame格式 后续剔除未知类型
# data2=data2.dropna() ##剔除异常的nan
data2 = data2[data2['TagType'].isin(
    ["BOOL", "REAL"]) | data2['TagName'].str.contains("Local:") & ~data2['TagName'].str.contains(":C")  ]##可以读取的类型 ["BOOL", "TIMER", "REAL","AB:Embedded_DiscreteIO:O:0","AB:Embedded_DiscreteIO:I:0"]
##剔除程序名和已知类型之外的数据
data2 = data2['TagName']
# print(data2[data2.str.contains("Local:")])
data2[data2.str.contains("Local:")]=data2[data2.str.contains("Local:")]+".Data"
# data2=np.where()
# data2.replace("Local:1:I","Local:1:I.Data",inplace=True)
# data2.replace("Local:1:O","Local:1:O.Data",inplace=True)

print(data2)