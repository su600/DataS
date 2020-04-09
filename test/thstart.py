import threading
import time
# global www

# @app.route("/test1",methods=["GET"])
# @is_login
class DownThread:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        i = 0
        while 1:
            i = i + 1
            print(i)
            time.sleep(1)

def aaa():
    print("main thread")
    t1 = threading.Thread(target=DownThread,args=())
    t1.setDaemon(True)
    t1.start()
    a=input()
    if a=="0":
        DownThread.terminate()
        print("End")

def fun():
    i=0
    while 1:
        i=i+1
        print(i)
        time.sleep(1)

aaa()