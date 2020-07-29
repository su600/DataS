import socket
# import sys
# import time

import logging
import asyncio

from asyncua import ua, Server


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def main():
    # setup our server
    print('***请确保机器人控制程序已启动，输入任意键继续 ***：')
    aaa = input()
    print('【正在初始化OPC UA Server...】')
    server = Server()
    await server.init()
    server.default_timeout = 60
    endpoint = 'opc.tcp://0.0.0.0:4840/'
    server.set_endpoint(endpoint)
    # server.set_endpoint('opc.tcp://192.168.100.173:4840/')
    # setup our own namespace, not really necessary but should as spec
    try:
        #################################
        # # 设置加密和密钥后 prosys可以连接 None方式不行
        await server.load_certificate("certificate.der")
        await server.load_private_key("private-key.pem")
    
    ## set all possible endpoint policies for clients to connect through
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

        x1 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔TCP坐标', '3:x_Drilling'])
        y1 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔TCP坐标', '3:y_Drilling'])
        z1 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔TCP坐标', '3:z_Drilling'])
        a1 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔TCP坐标', '3:a_Drilling'])
        b1 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔TCP坐标', '3:b_Drilling'])
        c1 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔TCP坐标', '3:c_Drilling'])

        A1 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔关节角度', '3:A1_Drilling'])
        A2 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔关节角度', '3:A2_Drilling'])
        A3 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔关节角度', '3:A3_Drilling'])
        A4 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔关节角度', '3:A4_Drilling'])
        A5 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔关节角度', '3:A5_Drilling'])
        A6 = await root.get_child(["0:Objects", "3:制孔机器人", '3:制孔关节角度', '3:A6_Drilling'])

        x2 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接TCP坐标', '3:x_Riveting'])
        y2 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接TCP坐标', '3:y_Riveting'])
        z2 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接TCP坐标', '3:z_Riveting'])
        a2 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接TCP坐标', '3:a_Riveting'])
        b2 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接TCP坐标', '3:b_Riveting'])
        c2 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接TCP坐标', '3:c_Riveting'])

        A7 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接关节角度', '3:A1_Riveting'])
        A8 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接关节角度', '3:A2_Riveting'])
        A9 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接关节角度', '3:A3_Riveting'])
        A10 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接关节角度', '3:A4_Riveting'])
        A11 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接关节角度', '3:A5_Riveting'])
        A12 = await root.get_child(["0:Objects", "3:铆接机器人", '3:铆接关节角度', '3:A6_Riveting'])

        actuator1 = await root.get_child(["0:Objects", "3:末端执行器", '3:主轴'])
        actuator2 = await root.get_child(["0:Objects", "3:末端执行器", '3:压脚'])
        actuator3 = await root.get_child(["0:Objects", "3:末端执行器", '3:滑台1'])
        actuator4 = await root.get_child(["0:Objects", "3:末端执行器", '3:滑台2'])

        normal1 = await root.get_child(["0:Objects", "3:法向", '3:B'])
        normal2 = await root.get_child(["0:Objects", "3:法向", '3:C'])
        normal3 = await root.get_child(["0:Objects", "3:法向", '3:D'])

        data_name = [x1, y1, z1, a1, b1, c1,
                     A1, A2, A3, A4, A5, A6,
                     x2, y2, z2, a2, b2, c2,
                     A7, A8, A9, A10, A11, A12,
                     actuator1, actuator2, actuator3, actuator4,
                     normal1, normal2, normal3]

        # 设置可写
        for i in data_name:
            await i.set_writable()

        print('\n')
        print('【OPC UA Server初始化完成】')
        print('【读取config.txt参数配置】')
        file = 'config.txt'
        try:
            with open(file) as f:
                lines = f.readlines()
                ip = lines[0].split(':')[1].strip()
                port = int(lines[1].split(':')[1])
                cycle = int(lines[2].split(':')[1])/1000
        except Exception as e:
            print(e)
        else:
            print(f'【开始与{ip}:{port}机器人程序建立连接】')
        
        # socket通信
        def socket_client(ip, port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
            except socket.error as e:
                print(f'Socket连接错误:{e} 请确认连接参数重新启动程序')
                # sys.exit(1)
            else:
                send_data = '0'
                s.send(send_data.encode())
                receive_data = s.recv(1024).decode()
                # kuka_data=data_analysis(send_data,receive_data)
                # print("收到信息", receive_data)
                # s.close()
                return receive_data

        # OPC UA 数据更新
        async with server:
            print(f'【OPC UA Server启动完成开始转发数据】')
            print(f'【OPC UA Server地址{endpoint} 采集周期{cycle * 1000}ms】')
            while True:
                await asyncio.sleep(cycle)  # 数据更新周期
                data = socket_client(ip, port)

                try:
                    n = 0
                    for i in data_name:
                        await i.write_value(data.split(',')[n])
                        n += 1
                except Exception as e:
                    # print(f'ERROR: {e}')
                    pass
                else:
                    pass

# todo 程序停止
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(main())
    loop.close()
