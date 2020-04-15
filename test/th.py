###### 多线程 daemon守护线程test
import time
import threading

def fun():
    for i in range(5):
        # print("start fun")
        time.sleep(1)
        print("fun1")

def fun2():
    while 1:
        time.sleep(1)
        print("end fun2")

def main():
    # print("main thread")
    t1 = threading.Thread(target=fun,args=())
    t2 = threading.Thread(target=fun2, args=())
    # t1.setDaemon(False)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    # time.sleep(2)
    # t1.join()
    # t2.join()
    # print("main thread end")

if __name__ == '__main__':
    main()
