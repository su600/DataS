import snap7.client as client
from snap7.util import *
from snap7.snap7types import *

def s7read():
    plc = client.Client()
    # print(ip,rack,slot)
    plc.connect("192.168.100.111", 0, 1)
    ss = ""  # 标识I/Q/M
    t = areas["PE"]
    variable = []
    data = []
    # print(address)
    address="0.1"
    if address == '':
        address2 = 0.0
    else:
        address2 = (float(address))
    if t == 129:
        ss = "I "
    if t == 130:
        ss = "Q "
    if t == 131:
        ss = "M "

    b = (int(address2))
    c = (int((address2 - b) * 10))

    # print(t,b,c)
    try:
        variable.append(ss + address)
        print(variable)
        # timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = plc.read_area(t, 0, b, 8)  ## 变量类型，0，地址起始，固定8位
        aa=plc.read_multi_vars(["I0.1","Q0.1"])
        print(aa)
        data.append(get_bool(result, 0, c))  ## 地址偏移值
        # tt0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    except Exception as e:
        print(e)
    else:
        siemensdata0 = dict(zip(variable, data))
        print(siemensdata0)
        # return siemensdata0, tt0

s7read()