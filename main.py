from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file,Blueprint
from flask_bootstrap import Bootstrap
from flask import copy_current_request_context
import random, datetime
from functools import wraps
import time
import functools
import os
from werkzeug.utils import secure_filename
import csv
import pandas as pd
import numpy as np
from struct import pack, unpack_from  # Pylogix 结构体解析

app = Flask(__name__)
Bootstrap(app)
# from blueprints.login import is_login

## 设置密钥可以有效防止跨站请求伪造的攻击
app.config['SECRET_KEY'] = 'myproject'
app.secret_key = 'myproject'

@app.route("/")
def home():
    return render_template("home.html")
    # time1=random.randint(1,10)
    # print(time1)
    # return render_template("home.html",time=time1)

# 在应用对象上注册蓝图对象
#3.在应用对象上注册这个蓝图对象
from blueprints.login import *
app.register_blueprint(login_)

## 设备选择界面
from blueprints.settings import *
app.register_blueprint(settings_)

## 西门子界面
from blueprints.siemens import *

app.register_blueprint(siemens_)

## 罗克韦尔
from blueprints.rockwell import *

app.register_blueprint(rockwell_)

## 倍福
from blueprints.beckoff import *

app.register_blueprint(beckoff_)

## OPC UA
from blueprints.opcua import *

app.register_blueprint(opcua_)

## influxDB
# global influxdata
from blueprints.influxdb import *

app.register_blueprint(influxdb_)


################### app 主程序 （测试用） 部署版本采用nginx托管 ##########################
# 其中debug的作用是方便调试用，利用nohup command &在后台启动程序，然后源代码修改后，自动加载。
# host设定为0.0.0.0是为了能够非本机访问，默认127.0.0.1，只能本机使用localhost访问。
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False,port=4000, threaded=True)