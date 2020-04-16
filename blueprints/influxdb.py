from flask import Flask,render_template,request,redirect, url_for, flash, session, send_from_directory,send_file
from flask_bootstrap import Bootstrap
import random,datetime
from functools import wraps
import time
import functools
import os
from werkzeug.utils import secure_filename
import csv
import pandas as pd
import numpy as np
from struct import pack, unpack_from # Pylogix 结构体解析

from flask import Blueprint
from blueprints.login import is_login

# from blueprints.siemens import s7read
from blueprints.rockwell import rockwellread
from blueprints.opcua import *

influxdb_ = Blueprint("influxdb_",__name__)

'''
influxDB 库文件
'''
from influxdb_client import InfluxDBClient,Point
# from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
import time

######################## InfluxDB 共用函数 #############################
@influxdb_.route("/influxDB",methods=("POST","GET"))
@is_login
def influxDB(influxdbip,token,measurement,cycle):
    print("influxDB写入")
    # a=1
    bucket = "data"
    token="HTvG6oIApfABybjjYd_6Jehf8AEWkLStYw0qftanx9ijF05-UsLZ9pVqI604PwuRlhv8IkuIZshYaqVFTC0DXA=="
    client = InfluxDBClient(url=influxdbip,token=token,org="su")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    # query_api = client.query_api()
    cycle=(int(cycle)/1000) #单位ms
    # cycle=(cycle)
    flash("开始写入influxDB","influx")
    while 1:
        try:
            # todo 不同品牌的设备 如何区分
            while 1:
                data = rockwellread()[1]
                # print(data, type(data))
                aa = list(range(0, len(data)))
                n = 0
                for i in data:
                    aa[n] = Point(measurement).tag("location", "108厂房").field(i, data[i])
                    n += 1
                # print(aa)
                write_api.write(bucket=bucket, org="su", record=aa)
                time.sleep(cycle)
        except Exception as e:
            print(e)
            break