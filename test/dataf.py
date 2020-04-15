import pandas as pd
import numpy as np

file="D:\Taglist 2020-03-27 15-59-12.xlsx"
data2 = pd.read_excel(file)  ##输出为DataFrame格式 后续剔除未知类型
# data2=data2.dropna() ##剔除异常的nan
data2 = data2[data2['TagType'].isin(
    ["BOOL", "REAL","AB:Embedded_DiscreteIO:O:0","AB:Embedded_DiscreteIO:I:0"])]  ##可以读取的类型 ["BOOL", "TIMER", "REAL","AB:Embedded_DiscreteIO:O:0","AB:Embedded_DiscreteIO:I:0"]
##剔除程序名和已知类型之外的数据
data2 = data2['TagName']
print(data2)

data2.replace("Local:1:I","Local:1:I.Data",inplace=True)
data2.replace("Local:1:O","Local:1:O.Data",inplace=True)

print(data2)