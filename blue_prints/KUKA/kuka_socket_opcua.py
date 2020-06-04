import socket
import sys
import time

import logging
import asyncio

from asyncua import ua, Server
from asyncua.common.methods import uamethod

import time

from pylogix import PLC

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

#
class KUKA_ROBOT:
    def __init__(self,ip,port,data):
        '''
        KUKA机器人对象
        :param ip: ip
        :param port: 端口 默认6008
        :param data: 数据
        '''
        self.ip=ip
        self.port=port
        self.data=[]

# global receive_data

async def main():
    # setup our server
    print('【正在初始化OPC UA Server...】')
    server = Server()
    await server.init()
    server.default_timeout=60
    server.set_endpoint('opc.tcp://0.0.0.0:4840/')
    # server.set_endpoint('opc.tcp://192.168.100.170:4840/')
    # setup our own namespace, not really necessary but should as spec
    try:
    #################################
    # # 设置加密和密钥后 prosys可以连接 None方式不行
        await server.load_certificate("certificate.der")
        await server.load_private_key("private-key.pem")
    #
    # # set all possible endpoint policies for clients to connect through
        server.set_security_policy([
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign])
    ########################################
    except Exception as e:
        print(e)

    else:

        uri = 'http://su600.cn'
        idx = await server.register_namespace(uri)

        # 导入xml文件
        await server.import_xml('kuka.xml')

        # 获取xml中的UA node
        # todo 待优化
        root = server.get_root_node()
        actuator1 = await root.get_child(["0:Objects", "0:Actuator", '0:actuator1'])
        actuator2 = await root.get_child(["0:Objects", "0:Actuator", '0:actuator2'])
        actuator3 = await root.get_child(["0:Objects", "0:Actuator", '0:actuator3'])
        actuator4 = await root.get_child(["0:Objects", "0:Actuator", '0:actuator4'])
        degree1 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Degree', '0:degree1'])
        degree2 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Degree', '0:degree2'])
        degree3 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Degree', '0:degree3'])
        degree4 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Degree', '0:degree4'])
        degree5 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Degree', '0:degree5'])
        degree6 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Degree', '0:degree6'])
        degree7 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree7'])
        degree8 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree8'])
        degree9 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree9'])
        degree10 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree10'])
        degree11 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree11'])
        degree12 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Degree_R', '0:degree12'])
        x1 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Joint', '0:x1'])
        x2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:x2'])
        y1 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Joint', '0:y1'])
        y2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:y2'])
        z1 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Joint', '0:z1'])
        z2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:z2'])
        a1 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Joint', '0:a1'])
        a2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:a2'])
        b1 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Joint', '0:b1'])
        b2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:b2'])
        c1 = await root.get_child(["0:Objects", "0:Drilling_Robot", '0:Joint', '0:c1'])
        c2 = await root.get_child(["0:Objects", "0:Riveting_Robot", '0:Joint_R', '0:c2'])
        normal1 = await root.get_child(["0:Objects", "0:Normals", '0:normal1'])
        normal2 = await root.get_child(["0:Objects", "0:Normals", '0:normal2'])
        normal3 = await root.get_child(["0:Objects", "0:Normals", '0:normal3'])

        data_name = [x1,y1,z1,a1,b1,c1,
                     degree1, degree2, degree3, degree4,degree5,degree6,
                     x2,y2,z2,a2,b2,c2,
                     degree7, degree8, degree9, degree10, degree11, degree12,
                     actuator1, actuator2, actuator3, actuator4,
                     normal1, normal2, normal3]

        # todo 设置可写
        for i in data_name:
            await i.set_writable()

        print('\n')
        print('【OPC UA Server初始化完成】')
        # todo 错误处理 自动重连
        print('***请确保机器人控制程序已启动,然后输入IP地址***：')
        ip = input()
        # print('请输入端口号(默认6008）：')
        # try:
        #     port = int(input())
        # except Exception as e:
        #     print(e, '端口号格式错误')
        #     print('请重新输入端口号')
        #     port = int(input())
        port=6008

        print('请输入采集周期(单位ms）：')
        try:
            cycle = int(input())/1000
        except Exception as e:
            print(e, '周期输入有误 请重新输入')
            # print('请重新输入端口号')
            cycle = int(input())/1000

        # socket通信
        def socket_client(ip, port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
            except socket.error as e:
                print(e)
                # sys.exit(1)
            else:
               # send_data = input('请输入发送命令: ').strip()
                send_data = '0'
                s.send(send_data.encode())
                receive_data = s.recv(1024).decode()
                # kuka_data=data_analysis(send_data,receive_data)
                # print("收到信息", receive_data)
                # s.close()
                return receive_data

        # OPC UA 数据更新
        async with server:
            # count = 0
            print('【OPC UA Server启动完成开始转发数据】')
            while True:
                # cycle=0.05
                await asyncio.sleep(cycle) # 数据更新周期
                data = socket_client(ip,port)

                n=0
                for i in data_name:
                    await i.write_value(data.split(',')[n])
                    n+=1

# todo 程序停止
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(main())
    loop.close()

