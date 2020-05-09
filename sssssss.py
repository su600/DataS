'''
    py file for test
'''
import pandas as pd
import ctypes
import struct

import snap7
from snap7.common import check_error
# from snap7.snap7types import S7DataItem, S7AreaDB, S7WLByte
from snap7.snap7types import *
from snap7 import util
import snap7
from snap7.common import check_error
# from snap7.snap7types import S7DataItem, S7AreaDB, S7WLByte
from snap7.snap7types import *
from snap7 import util

client = snap7.client.Client()
client.connect('192.168.100.111', 0, 1)
x=2
dataitemsgroup = []
for i in range(x):
    dataitemsgroup.append("data_items" + str(i))
print(dataitemsgroup)

for i in dataitemsgroup:
    aa=(S7DataItem * 3)()

print(aa)
print(aa[0:1])
aa=client.read_multi_vars(aa)