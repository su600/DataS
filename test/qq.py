'''
程序测试
'''
#列表平铺展开
vec = [[1,2,3],[4,5,6],[7,8,9]]
get = sum(vec,[])
print(get)
#列表合并为字典
a=[1,2,3,4]
b=["a","b","c","d"]
c=dict(zip(a,b))
print((c))

#字典索引
for a in c:
    print(a,c[a])
    # print(c.items())

# 字符串分割提取IP地址
aa='1769-L18ERM/B LOGIX5318ERM 192.168.100.200'
aa=aa.split(" ")
bb=aa[len(aa)-1] #获取ip
print(bb)
print(type(bb))

# pandas处理空行
import pandas as pd
import numpy as np
file="D:/Taglist 2020-04-01 08-48-34.xlsx"
data2 = pd.read_excel(file)
# print(data2)
# print(data2.head())
# print(data2.info())
# data2.dropna(axis=0, how='any', inplace=True)

data2=data2[data2['TagType'].isin(["BOOL"])]  #,"TIMER","REAL"]
# data2=data2['TagName']
# print(data2)
# data2.to_excel("D:/test2.xlsx",encoding='utf-8', index=False)
data2 = data2.to_numpy().tolist()  # 转数组 转列表
# global taglist
# taglist = sum(data2, [])  # 嵌套列表平铺 变量表list
print(data2)
# print(data2)