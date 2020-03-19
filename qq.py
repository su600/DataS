#
# import time
# print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
# 获取表单文件

from flask import Flask,render_template,request,redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
import random,datetime
from functools import wraps
import time
import functools
import os

from collections import OrderedDict
from pyexcel_xls import save_data
from pyexcel_xls import get_data
from pyexcel_xlsx import save_data
from pyexcel_xlsx import get_data
from flask.ext import excel

app=Flask(__name__)

@app.route("/",methods=["POST","GET"])
def test():

    if request.method=="POST":

        aa=request.files.get("file")
        data = get_data()
        print("数据格式：",type(data))
        for sheet_n in data.keys():
            print(sheet_n, ":", data[sheet_n])


    return render_template("2submit.html")

app.run()
