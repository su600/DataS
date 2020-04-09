###### 多线程 daemon守护线程test
import time
import threading


def fun():
    print("start fun")
    time.sleep(2)
    print("end fun")

def main():
    print("main thread")
    t1 = threading.Thread(target=fun,args=())
    t1.setDaemon(True)
    t1.start()
    time.sleep(1)
    print("main thread end")

if __name__ == '__main__':
    main()
