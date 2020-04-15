from flask import Flask, render_template,jsonify,request,redirect
import time
import threading
import inspect
import ctypes

app = Flask(__name__)

#
# def _async_raise(tid, exctype):
# 	"""raises the exception, performs cleanup if needed"""
# 	tid = ctypes.c_long(tid)
# 	if not inspect.isclass(exctype):
# 		exctype = type(exctype)
# 	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
# 	if res == 0:
# 		raise ValueError("invalid thread id")
# 	elif res != 1:
# 		# """if it returns a number greater than one, you're in trouble,
# 		# and you should call it again with exc=NULL to revert the effect"""
# 		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
# 		raise SystemError("PyThreadState_SetAsyncExc failed")
#
#
# def stop_thread(thread):
# 	_async_raise(thread.ident, SystemExit)
# @app.route("/", methods=["GET","POST"])
# def hh():
# 	if request.method == "POST":
# 		print("sssssssssssss")
# 		return redirect("a")
# 	else:
# 		while 1:
# 			pass
# 			return render_template("th.html")

@app.route("", methods=["GET","POST"])
def demo():
	def fun2():
		i=0
		while 1:
			i+=1
			time.sleep(1)
			print(i)

	def fun1():
		# a=1
		if request.method == "POST":
			print("sssssssssssss")


	t1 = threading.Thread(target=fun1, args=())
	t2 = threading.Thread(target=fun2, args=())
	t2.setDaemon(True)
	t1.start()
	t2.start()
	# if request.method=="POST":
	# 	stop_thread(myThread)
	return render_template("th.html")

@app.route("/b", methods=["GET","POST"])
def a():
	return "Stop"

if __name__ == "__main__":
	app.run()
