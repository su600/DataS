# Pandas解析AB PLC IO变量表

> 苏安东 2020-04-24

# Pandas库

### Pandas是什么

<img src="C:\Users\su514\AppData\Roaming\Typora\typora-user-images\image-20200424081449217.png" alt="image-20200424081449217" style="zoom: 40%;" />

<img src="C:\Users\su514\AppData\Roaming\Typora\typora-user-images\image-20200424082420834.png" alt="image-20200424082420834" style="zoom: 25%;" />GitHub https://github.com/pandas-dev/pandas  <img src="C:\Users\su514\AppData\Roaming\Typora\typora-user-images\image-20200424082320212.png" alt="image-20200424082320212" style="zoom: 20%;" />Pandas中文网 https://www.pypandas.cn/ 

> Pandas是一个强大的**分析结构化数据的工具集**,它的使用基础是Numpy（提供高性能的矩阵运算）；用于数据**挖掘和数据分析**，同时也提供**数据清洗**功能。Pandas是一个开源的、强大的 Python 数据分析支持库，BSD许可的库，为Python提供高性能、易于使用的数据结构和数据分析工具。

### Pandas解决什么问题

> Python在数据处理和准备方面一直做得很好，但在数据分析和建模方面就没那么好了。
> Pandas帮助填补了这一空白，在Python中执行整个数据分析工作流程，而不必切换到更特定于领域的语言。
> 与出色的 IPython 工具包和其他库相结合，Python中用于进行数据分析的环境在性能、生产率和协作能力方面都是卓越的。

### Pandas库的亮点

- 一个快速、高效的**DataFrame**对象，用于数据操作和综合索引；
- 用于在内存数据结构和不同格式之间**读写数据**的工具：CSV、TXT、Excel、SQL数据库等；
- 智能**数据对齐**和丢失数据的综合处理：在计算中基于标签的自动对齐，轻松地将凌乱的数据变有序的形式；
- 数据集的**灵活调整**和旋转；
- 基于智能标签的**切片、花式索引**和大型数据集的**子集**；
- 可以从数据结构中插入和删除列，以实现**大小可变**；
- 通过在强大的引擎中**聚合**或转换数据，允许对数据集进行拆分应用组合操作;
- 数据集的高性能**合并和连接**；
- **层次轴索引**提供了在低维数据结构中处理高维数据的直观方法；
- **时间序列**-功能：日期范围生成和频率转换、移动窗口统计、移动窗口线性回归、日期转换和滞后。甚至在不丢失数据的情况下创建特定领域的时间偏移和加入时间序列；
- 对**性能进行了高度优化**，用Cython或C编写了关键代码路径。
- Python与Pandas在广泛的**学术和商业**领域中使用，金融，经济学，统计学，广告，网络分析，等等。

> **这些功能主要是为了解决其它编程语言、科研环境的痛点。处理数据一般分为几个阶段：数据整理与清洗、数据分析与建模、数据可视化与制表，Pandas 是处理数据的理想工具。**

> **总结一下就是能想到的分析变换需求Pandas全支持，只有想不到没有做不到**

### DataFrame & Series

| 名称      | 维数 | 描述                               |
| :-------- | :--: | ---------------------------------- |
| Series    |  1   | 带标签的一维同构数组               |
| DataFrame |  2   | 带标签的，大小可变的，二维异构表格 |

*DataFrame是Pandas中的一个**表格型**的数据结构，包含有一组有序的列，每列可以是不同的值类型(数值、字符串、布尔型等)，DataFrame即有行索引也有列索引，可以被看做是由Series组成的字典。*

**起源**：最早的 "DataFrame" 来源于贝尔实验室开发的 S 语言。"data frame" 在 1990 年就发布了，书《S 语言统计模型》第3章里详述了它的概念，书里着重强调了 dataframe 的矩阵起源。书中描述 DataFrame 看上去很像矩阵，且支持类似矩阵的操作，同时又很像关系表。

**DataFrame实现：**R 语言作为 S 语言的开源版本，于 2000 年发布了第一个稳定版本，并且实现了 dataframe。Pandas 于 2009 年被开发，Python 中于是也有了 DataFrame 的概念。DataFrame 都同宗同源，有着相同的语义和数据模型。

**DataFrame 有几个独一无二的属性**

- 保证顺序，行列对称
- DataFrame 的 API 非常丰富
- 直观的语法，适合交互式分析
- 列中允许异构数据

> **DataFrame 的需求来源于把数据看成矩阵和表，DataFrame 可以理解成是关系系统、矩阵、甚至是电子表格程序（典型如 Excel）的合体。**

-----

# AB PLC IO变量表处理

### 问题背景

软件使用流程是:

- 连接到AB PLC，自动获取所有变量表 Excel
- 对变量表筛选需要采集的变量，上传修改后的变量表进行批量采集，并写入InfluxDB

> **PyLogix**读取回来的变量表中并非所有的原始变量名都可以直接读取，**尤其是IO变量，均无法直接读取**。

<u>原始IO Excel文件</u>

- 无法直接读取
- IO变量存在**大量冗余**
- DI/DO/AI/AO分类
- 单路/多路分类
- 16位/32位分类

<u>IO解析Excel文件</u>

> 需要根据读取的原始变量类型进行解析，随后进行相应的变换处理，最终由**原始变量表**得到**可以直接读取**的变量表，进而获得所有的IO信息。
> 属于**数据清洗**和**简单分析**，**Pandas是最佳途径。**

### 处理流程

1. 保留已知数据类型 `['BOOL','REAL','INT'等]`
2. 同时保留`Local:` 模块
3. 剔除 `:C` 变量（无用），剔除非IO模块
4. Output模块剔除Input变量，Input模块剔除Output变量
5. 重置当前DataFrame的索引
6. 正则表达式`re.findall` 从`TagType`提取IO类型
7. 正则表达式 ，进一步提取Ch表征 路数/位数，区分单路/一路
8. 根据Ch属性，对所有单路模块的`TagName`添加 `.Data`后缀，所有多路模块的`TagName`添加 `.Ch0Data`
9. DataFrame添加新行，将单变量扩充为多通道变量，对应所有多路模块添加 `.Ch1Data~.ChXData`

### Python代码

```python
def rockwellreadexcel():

    file="D:\IO原始列表.xlsx"
    data2 = pd.read_excel(file)  ##输出为DataFrame格式 后续剔除未知类型

    data2=data2.dropna() ##剔除异常的NAN

    # 剔除程序名,C变量 和已知类型之外的数据，保留IO变量
    data2 = data2[data2['TagType'].isin(["INT","DINT","BOOL", "REAL"])
                  | data2['TagName'].str.contains("Local:")
                  & ~data2['TagName'].str.contains(":C")
                  & ~data2['TagType'].str.contains("ASCII|MODULE") ]

    # 变量表中需要判断解析 生成相应的表变量名
    # 筛选变量 根据IO性质，剔除无用OI变量 （I的剔除O O的剔除I） 
    data2 = data2[(data2['TagType'].str.contains("I")   & 				~data2['TagType'].str.contains("O")) | (data2['TagType'].str.contains("O") & ~data2['TagType'].str.contains("I"))]
  
    data2=data2.reset_index(drop=True)  # 旧的索引依然存在 需要重新生成索引

    # 生成IOtype列 以下所有操作根据IOType进行 减少匹配和筛选
    import re #正则表达式库
    IOtype=data2['TagType'].to_numpy().tolist()
    IOtype=re.findall(r'_(.+?):', str(IOtype))
    data2.insert(2,'IOtype',IOtype) #添加一列作为IOType

    # 提取IOType 判断多路还是一路
    def IOTYPE(IOtype):
        Ch=[]
        for i in IOtype:
            ccc = (''.join(re.findall(r'\d+',str(i))))# 16/32位或路数 返回值为列表用join去除[]
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
    print(data2)

    ## 多个一样的模块 需要分别对应处理 嵌套循环 添加.ChXData
    ii=0
    for n in Ch: # 此处的Ch暂时是列表 不是数据表中的Ch列
        if ('one' in n) ==False :
            for i in range(1,int(n)): # range(1,8)=1~7 不包含8
               # 根据Ch0修改通道号 这里误替换了编号“10” 里面的0
                data2.loc[data2.shape[0]] = [(data2.loc[ii,'TagName']).replace('Ch0', 'Ch'+str(i))]
        ii += 1  # n的索引 对应各个Ch0Data
        
    print(f'处理耗时 {end - start} 秒')
    data2.to_excel('D:/Pandas_New_IO.xlsx',encoding='utf-8', index=False)  # 写入excel
    print("写入 D:/Pandas_New_IO.xlsx 完成")
```

<u>处理后Excel文件</u>

### 后续

**解析变换，得到了所有IO模块后直接可读取的TagName**，后续`rockwellread()`处理：

- [x] ['TagName'，’Ch‘] 筛选
- [ ] 根据Ch列的值，判断16位/32位
  
- [x] Digital格式化为二进制 取逆序 加 `/`
  - [ ] 区分16位/32位
  - [x] 可以不区分 数据正确 但是显示位数有问题
- [x] Analog根据量程转换为模拟量
- [ ] 仅基于已有模块类型推断解析，未知模块类型可能解析有误
- [ ] 其它变量解析 比如Timer/Counter/Axis等解析
- [ ] 对于较大的数据集来说Panda速度慢
  - [x] 处理耗时 0.1406247615814209 秒
- [ ] Pandas应用于数据分析处理

> **官方文档，程序优化，迭代逻辑优化，Pandas其它功能，where/mask/apply等**

---

