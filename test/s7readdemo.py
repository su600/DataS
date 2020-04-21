import snap7.client as c
from snap7.util import *
from snap7.snap7types import *


'''
S7AreaPE = 0x81 输入
S7AreaPA = 0x82 输出
S7AreaMK = 0x83 M
S7AreaDB = 0x84 DB
S7AreaCT = 0x1C 计数器
S7AreaTM = 0x1D 计时器

areas = ADict({
    'PE': 0x81,
    'PA': 0x82,
    'MK': 0x83,
    'DB': 0x84,
    'CT': 0x1C,
    'TM': 0x1D,
})
'''
def read(plc,b,c,t):
    while 1:
        try:
            result=plc.read_area(t,0,b,8)  ## 变量类型，0，地址起始，固定8位
        except Exception as e:
            print(e, "变量类型输入错误")
        else:
            return get_bool(result,0,c) ## 地址偏移值
            break

def ch(address):

    # address1=address.split(".")[1]
    # I 10.2, t=I,b=10,c=2
    try:
        t=(address[0])
        b=int((address.split(".")[0][1:]))
        c=int((address.split(".")[1]))
    except Exception as a:
        ## 万能异常处理
        print("变量地址格式输入不正确",a)
    # except (ValueError,TypeError,IndexError):
    #     print("变量地址输入格式不正确")
    else:
        if t is "i" or t is "I":
            t = areas["PE"]
        elif t is "q" or t is "Q":
            t = 0x82
        elif t is "m" or t is "M":
            t = 0x83
        else:
            t = "none"
        return (t,b,c)
    return


if __name__=="__main__":

    '''
    获取CPU信息并解码
    a=plc.get_cpu_info()
    a=struct.unpack("33s25s25s25s27s",a)
    print(a) 
    b=plc.get_cpu_state()
    print(b)
    ##########################################
    '''
    while 1:
        try:
            print("请输入PLC的IP地址 默认rack0，slot1，端口102：")
            ip = input()
            plc = c.Client()
            plc.connect(ip, 0, 1)
            # plc.disconnect() ## 断开连接
        except Exception as e:
            print(e,"连接失败，请重新输入！或检查网络连通性")
        except KeyboardInterrupt:
            exit()
        else:
            while 1:
                print("请输入变量地址：")
                address = input()
                t,b,c=ch(address)
                # print(t,b,c)
                print("地址 %s的值是"%address,"%s"% read(plc,b,c,t))
                print("\n")
                # break
