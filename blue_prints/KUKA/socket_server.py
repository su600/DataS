"""
file: service.py
socket service
"""

import socket
import threading
import time
import sys


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 6008))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Waiting connection...')

    while 1:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print(f'Accept new connection from {addr}')
    # conn.send(('Hi, Welcome to the server!').encode())
    while 1:
        data = conn.recv(1024).decode()
        # ss=data.decode('gbk')
        # print(data)
        if data == '1':
            ss='制孔六轴，123.22，234.3，123.65，234.12，123.21，123.32'
        elif data == '2':
            ss = '制孔角度，123.22，234.3，123.65，234.12，123.21，123.32'
        elif data == '3':
            ss = '铆接六轴，123.22，234.3，123.65，234.12，123.21，123.32'
        elif data == '4':
            ss = '铆接角度，123.22，234.3，123.65，234.12，123.21，123.32'
        elif data == '5':
            ss = '末端状态，1，2，3，4，5，6'
        elif data == '6':
            ss = '相机，No images'
        else:
            ss='无效命令'+data
        print(f'{addr} client send data is {data}')  # b'\xe8\xbf\x99\xe6\xac\xa1\xe5\x8f\xaf\xe4\xbb\xa5\xe4\xba\x86'
        time.sleep(0.05) # 50ms
        if data == 'exit' or not data:
            print(f'{addr} connection close')
            conn.send(bytes('Connection closed!'), 'UTF-8')
            break
        # conn.send(bytes('{0}'.format(ss), "UTF-8"))  # TypeError: a bytes-like object is required, not 'str'
        conn.send(bytes(ss.encode('UTF-8')))
    conn.close()


if __name__ == '__main__':
    socket_service()