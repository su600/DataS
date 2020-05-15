import logging
import asyncio

from asyncua import ua, Server
from asyncua.common.methods import uamethod

import time

from pylogix import PLC

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

#
class Rockwell_AB_PLC:
    def __init__(self,IP,tag_list):
        '''
        Rockwell AB PLC 对象
        :param IP:  PLC IP地址
        :param tag_list:  变量表
        '''
        self.IP=IP
        self.tag_list=tag_list

class Siemens_PLC:
    def __init__(self, IP, slot ,tag_type, tag_address, data_type, tag_name ):
        '''
        西门子PLC对象
        :param IP:
        :param slot:
        :param tag_type: I、M、Q
        :param tag_address: 地址 0.1
        :param data_type: 数据类型 Bool,Read ...
        :param tag_name:  变量名
        '''
        self.IP = IP
        self.slot = slot
        self.tag_list = tag_list

    # def read(self):
    #     with PLC() as plc:
    #         plc.IPAddress = self.IP
    #         while 1:
    #             try:
    #                 print('读取')
    #                 aa = plc.Read(self.tag_list)
    #                 # print(aa.TagName,aa.Value)
    #                 time.sleep(self.cycle)
    #             except Exception as e:
    #                 print(e)
    #             else:
    #                 return aa
    #
    # def kill_threads(self):
    #     self.threadStatus = False
    #
    # def run_threads(self):
    #     self.threadStatus = True
    #     self.threads['update_server'] = threading.Thread(target=self.read())
    #     self.threads['update_server'].start()


def Read(IP,tag_list):
    '''
    Rockwell AB PLC 数据读取函数
    不超过10个变量

    :param IP: AB PLC的IP
    :param tag_list: 待读取的变量表
    :param cycle: 读取周期
    :return: 变量采集结果 含 .TagName/.Value/.Status
    '''
    with PLC() as plc:
        plc.IPAddress = IP
        while 1:
            try:
                print('读取')
                ret=plc.Read(tag_list)
                # print(aa.TagName,aa.Value)
                # time.sleep(cycle)
            except Exception as e:
                print(e)
            else:
                return ret

@uamethod
def func(parent, value):
    return value * 2

def rockwellread(IP,tag_list):    #'读取函数'
    # print("readlist")
    # print("taglist",taglist)
    ### 分批读取函数 每次读取10个变量
    def readten(tag_list):
        l = len(tag_list)  # 变量表长度，如果大于10 必须分批读取保证不报错
        x,y=divmod(l,10) # Python内置函数返回 整除和余数
        if x==0:x=1
        a = 0  # 每一组变量的上标
        val = []  # 初始化列表 每一组变量值
        # print(tag_list,'11111')
        for n in range(x):
            if n < x:
                # print(tag_list)
                val = val + comm.Read(tag_list[10 * a:10 * (a + 1)])
                a += 1
                n += 1
            if n == x and y != 0:
                val = val + comm.Read(tag_list[10 * a:10 * a + y])
        vall = val
        # print(vall)
        return vall

    with PLC() as comm:
        # while 1:
        tagname=[]
        tagvalue=[]
        comm.IPAddress = IP
        ret=readten(tag_list) #调用函数分批读取变量
        ttt=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for a in ret:
            tagname.append(a.TagName)
            tagvalue.append(a.Value)
        # print(tagname,tagvalue)

        return tagname,tagvalue

async def main():
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://0.0.0.0:4840/freeopcua/server/')
    # setup our own namespace, not really necessary but should as spec
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # await server.import_xml('device.xml')
    # # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()


    suobj=await objects.add_object(idx,'ROCKWELLObj')
    suvar=[]

    device=Rockwell_AB_PLC
    device.IP = '192.168.100.200'
    device.tag_list = ['Program:MainProgram.run', 'Program:MainProgram.start', 'Program:MainProgram.EMG',
                       'Local:1:O.Data.0', 'Local:1:O.Data.1', 'Local:1:O.Data.2','Local:1:O.Data.3', 'Local:1:O.Data.4',
                       'Local:1:O.Data.5','Local:1:O.Data.6', 'Local:1:O.Data.7']
    # 初始化 创建 opc ua变量
    a=0
    for i in device.tag_list:
        suvar.append(i)
        suvar[a]=await suobj.add_variable(idx,i,0) # fixme 初始化都写0
        await suvar[a].set_writable()
        a+=1

    # await objects.add_method(
    #     ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2),
    #     func, [ua.VariantType.Int64], [ua.VariantType.Int64]
    # )
    # _logger.info('Starting server!')
    async with server:
        count = 0
        while True:
            await asyncio.sleep(1) # 数据更新周期
            # print(device.IP,device.tag_list)
            aa,bb = rockwellread(device.IP,device.tag_list)
            # print(cc.Value)
            # print(aa,bb)
            # count += 0.1
            # _logger.info(aa, bb)
            # await myvar.write_value(count)
            a=0
            for i in bb:
                await suvar[a].write_value(i)
                a+=1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(main())
    loop.close()
