'''
仅socket程序 循环发送1~7
20200603 更新为发0 打包所有信息
'''
import socket
import sys
import time


def socket_client(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
    except socket.error as e:
        print(e)
        # sys.exit(1)
    else:
        # while 1:
            # send_data = input('请输入发送命令: ').strip()
        # send_data = ['0', '2', '3', '4', '5', '6', '7']
        send_data='0'
        s.send(send_data.encode())
        receive_data = s.recv(1024).decode()
        data_list = receive_data.split(',')
        print("收到信息", data_list[0:6])
        print("收到信息", data_list[6:12])
        print("收到信息", data_list[12:18])
        print("收到信息", data_list[18:24])
        print("收到信息", data_list[24:28])
        print("收到信息", data_list[28:31])
        print("收到信息", data_list[31])
    # s.close()

def start():
    print('请输入机器人IP地址：')
    ip = input()
    print('请输入端口号：')
    try:
        port = int(input())
    except Exception as e:
        print(e, '端口号格式错误')
        print('请重新输入端口号')
        port = int(input())
    else:
        socket_client(ip, port)

if __name__ == '__main__':
    start()
