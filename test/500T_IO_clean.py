'''
Pandas处理AB PLC IO变量表 精简版程序 仅处理并生成新的变量表
删掉之前测试的代码 仅保留最终代码
'''

import pandas as pd
import time

def rockwellreadexcel():
    start = time.time()
    file="D:\IO原始列表.xlsx"
    # data2 = pd.read_excel(file, usecols=[0], header=None)  ##第一列 无表头 输出为DataFrame格式 带索引
    data2 = pd.read_excel(file)  ##输出为DataFrame格式 后续剔除未知类型

    data2=data2.dropna() ##剔除异常的nan

    # 变量筛选 不算是完全通用的筛选方式  ##剔除程序名,C变量 和已知类型之外的数据，保留IO变量
    # isin()删选非IO变量  data2['TagType'].isin(["INT","DINT","BOOL", "REAL","COUNTER","TIMER","DWORD"]) 变量筛选
    data2 = data2[data2['TagType'].isin(["INT","DINT","BOOL", "REAL"])
                  | data2['TagName'].str.contains("Local:")
                  & ~data2['TagName'].str.contains(":C")
                  & ~data2['TagType'].str.contains("ASCII|MODULE") ]

    # todo 变量表中需要判断解析 生成相应的表变量名
    # 筛选变量 根据IO性质，剔除无用OI变量 （I的剔除O O的剔除I） 也可以写为 data2.TagType 不过看起来不够明显，修改不方便
    data2 = data2[(data2['TagType'].str.contains("I")   & ~data2['TagType'].str.contains("O"))
                  | (data2['TagType'].str.contains("O") & ~data2['TagType'].str.contains("I"))]

    data2=data2.reset_index(drop=True)  # todo 实际数据列表的数据删除了 但是旧的索引依然存在 需要重新生成索引

    # todo 生成IOtype列 以下所有操作根据IOType进行 减少匹配和筛选
    import re #正则表达式库
    IOtype=data2['TagType'].to_numpy().tolist()
    IOtype=re.findall(r'_(.+?):', str(IOtype))
    data2.insert(2,'IOtype',IOtype) #添加一列作为IOType

    # todo 提取IOType 判断多路还是一路
    def IOTYPE(IOtype):
        Ch=[]
        for i in IOtype:
            ccc = (''.join(re.findall(r'\d+', str(i))))# 点数 16位或 32位 或路数 返回值为列表 用join去除[]
            if i[0] == "I" or i[0] == "O": # 判断是否是多路 第一位是I,O就是多路
                Ch.append(ccc)
            else:
                Ch.append('one'+str(ccc))
        # 考虑one32，Ch所有值统一为字符串 否则筛选会报错
        return Ch

    Ch=IOTYPE(IOtype)
    data2.insert(3,'Ch',Ch) #添加一列作为IOType

    data2.loc[data2.Ch.str.contains("one"),'TagName'] += '.Data'
    data2.loc[~data2.Ch.str.contains("one"),'TagName'] += ".Ch0Data"
    # print(data2)

    ## todo 两个一样的模块 需要分别对应处理 嵌套循环 添加.ChXData
    ii=0
    for n in Ch: # 此处的Ch暂时是列表 不是数据表中的Ch列
        if ('one' in n) ==False :
            for i in range(1,int(n)): # range(1,8)=1~7 不包含8
                # 这里误替换了编号“10” 里面的0 修改替换字段位'Ch0'
                data2.loc[data2.shape[0]] = [(data2.loc[ii, 'TagName']).replace('Ch0', 'Ch' + str(i)),
                                             data2.loc[ii, 'TagType'], data2.loc[ii, 'IOtype'], data2.loc[ii, 'Ch']]
        ii += 1  # n的索引 对应各个Ch0Data

    end = time.time()
    print(f'处理耗时 {end - start} 秒')

    print(data2)
    data2.to_excel('D:/Pandas_New_IO.xlsx', encoding='utf-8', index=False) #写入excel

start = time.time()

rockwellreadexcel()

end = time.time()
print(f'处理耗时 {end - start} 秒')