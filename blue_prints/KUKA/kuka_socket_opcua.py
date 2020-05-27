import socket
import sys
import time


def socket_client(ip,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
    except socket.error as e:
        print(e)
        # sys.exit(1)
    else:
    # print(s.recv(1024))  # 目的在于接受：Accept new connection from (...
        i=0
        while 1:
            # send_data = input('请输入发送命令: ').strip()
            send_data=['1','2','3','4','5','6','7']
            s.send(send_data[i].encode())
            i+=1
            if i==7:i=0
            receive_data=s.recv(1024).decode()
            # kuka_data=data_analysis(send_data,receive_data)
            print("收到信息",receive_data)
            time.sleep(0.1)

        s.close()



def start():
    print('请输入机器人IP地址：')
    ip=input()
    print('请输入端口号：')
    try:
        port=int(input())
    except Exception as e:
        print(e,'端口号格式错误')
        print('请重新输入端口号')
        port=int(input())
    else:
        socket_client(ip,port)


if __name__ == '__main__':
    start()
