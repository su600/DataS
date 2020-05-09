from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file,Blueprint,jsonify
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

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)

# from blueprints.login import is_login
## 设置密钥可以有效防止跨站请求伪造的攻击
app.config['SECRET_KEY'] = 'myproject'
app.secret_key = 'myproject'

app.config['SECRET_KEY'] = 'f1d9d48ec0e26e2a250839fa36ea2c602cc4f85ccfeb5c65'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #todo SQLite 数据库用于账号管理和变量表存储 参考自 s7 opcserver
# from flask_wtf.csrf import CSRFProtect
# csrf = CSRFProtect(app)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")

# 在应用对象上注册蓝图对象
#3.在应用对象上注册这个蓝图对象
from blue_prints.LOGIN.login import login_

app.register_blueprint(login_)

## 设备选择界面
from blue_prints.SETTINGS.settings import settings_

app.register_blueprint(settings_)

## 西门子界面
from blue_prints.SIEMENS.siemens import siemens_

app.register_blueprint(siemens_)

## 罗克韦尔
from blue_prints.ROCKWELL.rockwell import rockwell_

app.register_blueprint(rockwell_)

## 倍福
from blue_prints.BECKOFF.beckoff import beckoff_

app.register_blueprint(beckoff_)

## OPC UA
from blue_prints.OPCUA.opcua import opcua_

app.register_blueprint(opcua_)

## influxDB
from blue_prints.INFLUXDB.influxdb import influxdb_

app.register_blueprint(influxdb_)


################### app 主程序 （测试用） 部署版本采用nginx托管 ##########################
# 其中debug的作用是方便调试用，利用nohup command &在后台启动程序，然后源代码修改后，自动加载。
# host设定为0.0.0.0是为了能够非本机访问，默认127.0.0.1，只能本机使用localhost访问。
# todo nginx托管
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False,port=4000, threaded=True)