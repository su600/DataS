'''
Python局域网扫描获取存活主机的IP by 郑瑞国  su 仅能显示ip
1、获取本机操作系统名称
2、获取本机IP地址
3、ping指定IP判断主机是否存活
4、ping所有IP获取所有存活主机
'''
import platform
import socket
import os
import threading
import time
import sys


def my_os():  # 1、获取本机操作系统名称
    return platform.system()


def my_ip():  # 2、获取本机IP地址
    return socket.gethostbyname(socket.gethostname())


def ping_ip(ip):  # 3、ping指定IP判断主机是否存活
    if my_os() == 'Windows':
        p_w = 'n'
    elif my_os() == 'Linux':
        p_w = 'c'
    else:
        print('不支持此操作系统')
        sys.exit()
    output = os.popen('ping -%s 1 %s' % (p_w, ip)).readlines()
    for w in output:
        if str(w).upper().find('TTL') >= 0:
            print(ip, 'ok')


def ping_all(ip):  # 4、ping所有IP获取所有存活主机
    pre_ip = (ip.split('.')[:-1])
    for i in range(1, 256):
        add = ('.'.join(pre_ip) + '.' + str(i))
        # ping_ip(add)
        threading._start_new_thread(ping_ip, (add,))
        time.sleep(0.01)


if __name__ == '__main__':
    ping_all(my_ip())
